import asyncio
from app import App, AppConfig
import os


async def main():
  config: AppConfig = {"static_path": os.environ.get("STATIC_PATH")}
  app = App(config).make_app()
  app.listen(8080)
  await asyncio.Event().wait()


if __name__ == "__main__":
  asyncio.run(main())
