from flask import Flask, render_template, request, flash, redirect, session
from UserInterface import *
import time

myapp = Flask(__name__)
myapp.secret_key = "abc"

@myapp.route("/")
def homepage():
    return render_template("homepage.html")  # This is the login page that they first see

@myapp.route("/", methods = ["POST"])
def checklogin():
    # Retrieve the data
    email = request.form['Email']
    password = request.form['Password']
    error, message = login(email, password)
    if error:
        flash(message)  # Output Alert
        return render_template("homepage.html", error=True)
    else:
        session['email'] = email
        return redirect('/welcome')

@myapp.route("/register", methods=["GET", "POST"])
def registerpage():
    if request.method == "POST":
        # Retrieve the data
        demail = request.form['DEmail']
        dpassword = request.form['DPassword']
        error, message = register(demail, dpassword)
        if error:
            flash(message)  # Output alert
            return render_template("register.html", error=True)
        else:
            session['email'] = demail  # Ensure that email is passed onto the next page
            return redirect('/welcome')
    return render_template("register.html")

@myapp.route("/welcome", methods=["GET", "POST"])
def welcomepage():
    # Create an object for the user
    email = session.get('email', None)
    user = UserInterface(email)
    if request.method == "POST":
        return render_template("loggedIn.html", prices=display_prices(), alerts=user.display_alerts())
    return render_template("loggedIn.html", prices=display_prices(), alerts=user.display_alerts())

if __name__ == "__main__":
    myapp.run(debug=True)