from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from flask_moment import Moment
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"

moment = Moment(app)


class NameEmailForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField(
        "What is your UofT Email address?",
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField("Submit")

    def validate_email(self, field):
        if "utoronto" not in field.data.lower():
            raise ValidationError("Please enter a UofT email address.")


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameEmailForm()

    if form.validate_on_submit():
        session["user_name"] = form.name.data
        session["user_email"] = form.email.data

        return redirect(url_for("chat_page"))

    return render_template("index.html", form=form)


@app.route("/chat")
def chat_page():
    if "user_name" not in session or "user_email" not in session:
        return redirect(url_for("index"))

    return render_template(
        "chat.html",
        user_name=session.get("user_name")
    )

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]

    if message.lower().startswith("my name is "):
        name = message[11:].strip()
        session["remembered_name"] = name
        reply = f"Nice to meet you, {name}!"

    elif "what is my name" in message.lower():
        remembered_name = session.get("remembered_name")

        if remembered_name:
            reply = f"Your name is {remembered_name}."
        else:
            reply = "I don't remember your name yet."

    elif "hello" in message.lower():
        reply = "Hello!"

    else:
        reply = "I don't understand."

    return jsonify({"reply": reply})


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)