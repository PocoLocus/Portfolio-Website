from flask import Flask, url_for, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from smtplib import SMTP
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

text_subtype = 'plain'

bootstrap = Bootstrap5(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/project_1")
def project_1():
    return render_template("project_1.html")

@app.route("/project_2")
def project_2():
    return render_template("project_2.html")

@app.route("/project_3")
def project_3():
    return render_template("project_3.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        content = (f"The user {form.name.data} sent you a message: {form.message.data}\n"
                   f"You can contact him/her through email at: {form.email.data}")
        msg = MIMEText(content)
        msg["Subject"] = "New message from your Portfolio Website"
        msg["From"] = os.getenv("SENDER_EMAIL")
        msg["To"] = os.getenv("RECEIVER_EMAIL")
        with SMTP(os.getenv("SMTPSERVER")) as connection:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
            connection.login(os.getenv("SENDER_EMAIL"), os.getenv("PASSWORD"))
            connection.sendmail(os.getenv("SENDER_EMAIL"), os.getenv("RECEIVER_EMAIl"), msg.as_string())
        return redirect(url_for("home"))
    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
