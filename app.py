from flask import Flask, render_template
from flask_moment import Moment
from datetime import datetime, timezone

app = Flask(__name__)
moment = Moment(app)


@app.route("/")
def index():
    return render_template(
        "index.html",
        current_time=datetime.now(timezone.utc)
    )


@app.route("/user/<name>")
def user(name):
    return f"<h1>Hello, {name}!</h1>"


if __name__ == "__main__":
    app.run(debug=True)