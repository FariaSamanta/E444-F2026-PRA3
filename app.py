from flask import Flask, render_template
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
    name = None
    email = None

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

    return render_template(
        "index.html",
        form=form,
        name=name,
        email=email
    )


if __name__ == "__main__":
    app.run(debug=True)