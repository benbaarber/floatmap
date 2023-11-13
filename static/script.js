class Ball {
  constructor(canvas, ctx, x, y, r, color) {
    this.canvas = canvas;
    this.ctx = ctx;
    this.x = x;
    this.y = y;
    this.r = r;
    this.color = color;
  }

  update(x, y) {
    this.x = (1 - x) * this.canvas.width
    this.y = y * this.canvas.height
  }

  draw() {
    this.ctx.fillStyle = this.color;
    this.ctx.beginPath()
    this.ctx.ellipse(this.x, this.y, this.r, this.r, 0, 0, 2*Math.PI)
    this.ctx.fill()
  }
}

class Connector {
  constructor(canvas, ctx, b1, b2, color) {
    this.canvas = canvas;
    this.ctx = ctx;
    this.b1 = b1;
    this.b2 = b2;
    this.color = color;
  }

  draw() {
    let d  = Math.hypot(this.b2.x - this.b1.x, this.b2.y - this.b1.y)
    let thickness = d < 200 ? (2 * (1 - d/200)) : 0

    if (thickness) {   
      this.ctx.strokeStyle = this.color;
      this.ctx.lineWidth = thickness;
      this.ctx.beginPath();
      this.ctx.moveTo(this.b1.x, this.b1.y);
      this.ctx.lineTo(this.b2.x, this.b2.y);
      this.ctx.stroke();
    }
  }
}

const main = () => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = 700;
  canvas.height = 700;

  const thumbBall = new Ball(canvas, ctx, 400, 350, 25, "blue");
  const pointerBall = new Ball(canvas, ctx, 350, 350, 25, "red");

  const balls = [thumbBall, pointerBall]

  const connector = new Connector(canvas, ctx, thumbBall, pointerBall, "purple")

  const ws = new WebSocket("ws://localhost:8080/websocket");
  ws.onopen = (e) => {
    console.log("WEBSOCKET OPEN")
  }
  ws.onmessage = (e) => {
    const { data } = JSON.parse(e.data)
    // console.log(data)
    if (data) {
      const { pointer, thumb } = data;
      pointerBall.update(...pointer)
      thumbBall.update(...thumb)
    }
  };
  ws.onerror = (e) => {
    console.log(e)
  }

  let last = 0
  const animate = (time = 0) => {
    last ||= time;
    if (time - last > 20) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const ball of balls) {
        ball.draw()
      }
      connector.draw()
      last = time;
    }
    window.requestAnimationFrame(animate);
  }

  animate()
}

window.onload = main