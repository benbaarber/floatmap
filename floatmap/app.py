import asyncio
import json
from tornado.web import StaticFileHandler, Application
from tornado.websocket import WebSocketHandler
from typing import TypedDict
from concurrent.futures import ThreadPoolExecutor
import os
from numpy.typing import NDArray
from fm import Floatmap


class FloatmapWebSocket(WebSocketHandler):
  def initialize(self, singleton) -> None:
    self.floatmap = singleton.get("floatmap")
    self.sockets: list[FloatmapWebSocket] = singleton["sockets"]
    self.thread = None

  def open(self):
    print("Websocket opened")
    self.sockets.append(self)

  def on_message(self, message):
    pass

  def on_close(self) -> None:
    print("Websocket closed")
    self.sockets.remove(self)


class AppConfig(TypedDict):
  static_path: str


class App:
  def __init__(self, config: AppConfig) -> None:
    self.static_path = config.get("static_path")
    self.pool = ThreadPoolExecutor(max_workers=os.cpu_count())
    self.sockets: list[FloatmapWebSocket] = []
    self.floatmap = Floatmap()

    async def callback(data: NDArray):
      data = data.tolist()
      if len(data) > 0:
        data = {"pointer": data[0][8], "thumb": data[0][4]}
      else:
        data = None
      serialized = json.dumps(dict(data=data))
      print(data)
      await asyncio.gather(
        *[
          asyncio.wrap_future(socket.write_message(serialized))
          for socket in self.sockets
        ]
      )

    loop = asyncio.get_event_loop()
    loop.run_in_executor(self.pool, self.floatmap.record, callback)

  def make_app(self):
    singleton = {"floatmap": self.floatmap, "sockets": self.sockets}

    routes = [
      (r"/websocket", FloatmapWebSocket, dict(singleton=singleton)),
      (
        r"/(.*)",
        StaticFileHandler,
        dict(path=self.static_path, default_filename="index.html"),
      ),
    ]

    return Application(routes, static_path=self.static_path)
