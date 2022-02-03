from flask import Flask, render_template, request, flash, redirect, session
import concurrent.futures
from AlertMonitor import *
from UserInterface import *

executor = concurrent.futures.ThreadPoolExecutor()

myapp = Flask(__name__)
myapp.secret_key = "abc"


@myapp.route("/")
def homepage():
    return render_template("homepage.html")  # This is the login page that they first see


@myapp.route("/", methods=["POST"])
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

@myapp.route('/logout')
def logout():
    #  Remove data from sessions
    session.pop('email', None)
    return redirect('/')

@myapp.route("/welcome", methods=["GET"])
def welcomepage():
    # Create an object for the user
    email = session.get('email', None)
    user = UserInterface(email)
    ids, alerts = user.display_alerts()
    return render_template("loggedIn.html", prices=display_prices(), ids=ids, alerts=alerts)

@myapp.route('/delete/<id>')
def delete(id):
    # Delete the alert
    alert = AlertMonitor(id)
    alert.delete_alert()
    return redirect("/welcome")


@myapp.route('/addAlerts')
def add_alerts_page():
    # Display the page
    return render_template("addAlertPage.html")


@myapp.route('/addAlertType1', methods=['POST'])
def add_alert_type1():
    # Add alert type 1
    email = session.get('email', None)
    user = UserInterface(email)
    coin = request.form.get('coin')
    price = request.form['price'].replace(',', '')  # remove commas
    if coin == 'Select Cryptocurrency':  # If they have not selected a coin
        flash('Please select a coin', 'danger')
    elif not price.replace('.', '').isdigit():  # If they have not entered a valid price
        flash('Please enter a valid price', 'danger')
    elif float(price) > 1000000:  # If the price is too big
        flash('Enter a price less than 1 million', 'danger')
    else:
        price = str(round(float(price), 4))  # round to 4 dp
        alertID = user.add_alert_type1(coin, price)
        alert = AlertMonitor(alertID)
        executor.submit(alert.monitor_alert)
        flash('The alert has been added successfully!', 'success')
    return redirect('/addAlerts')


@myapp.route('/addAlertType2', methods=['POST'])
def add_alert_type2():
    # Add alert type 2
    email = session.get('email', None)
    user = UserInterface(email)
    coin = request.form.get('coin')
    increasedOrDecreased = request.form.get('increasedOrDecreased')
    percentage = request.form['percentage'].replace(',','').replace('%', '')  # remove percentage symbols and commas
    if coin == 'Select Cryptocurrency':  # If they have not selected a coin
        flash('Please select a coin', 'danger')
    elif increasedOrDecreased == 'increased/decreased':  # If they have not selected increased or decreased
        flash("Please select 'increased' or 'decreased'", 'danger')
    elif not percentage.replace('.', '').isdigit():  # If they have not entered a valid percentage
        flash('Please enter a valid percentage', 'danger')
    elif float(percentage) > 1000000:  # If the percentage is too big
        flash('Enter a percentage less than 1 million', 'danger')
    else:
        percentage = round(float(percentage), 2)  # round to 2 dp
        alertID = user.add_alert_type2(coin, increasedOrDecreased, percentage)
        alert = AlertMonitor(alertID)
        executor.submit(alert.monitor_alert)
        flash('The alert has been added successfully!', 'success')
    return redirect('/addAlerts')


@myapp.route('/addAlertType3', methods=['POST'])
def add_alert_type3():
    # Add alert type 3
    email = session.get('email', None)
    user = UserInterface(email)
    coin = request.form.get('coin')
    daysAgo = request.form.get('daysAgo')
    highestOrLowest = request.form.get('highestOrLowest')
    if coin == 'Select Cryptocurrency':  # If they have not selected a coin
        flash('Please select a coin', 'danger')
    elif daysAgo == 'Select Days Ago':  # If they have not number of days ago
        flash('Please select the number of days ago', 'danger')
    elif highestOrLowest == 'highest/lowest':  # If they have not selected highest or lowest
        flash("Please select 'highest' or 'lowest'", 'danger')
    else:
        alertID = user.add_alert_type3(coin, int(daysAgo), highestOrLowest)
        alert = AlertMonitor(alertID)
        executor.submit(alert.monitor_alert)
        flash('The alert has been added successfully!', 'success')
    return redirect('/addAlerts')


@myapp.route('/addAlertType4', methods=['POST'])
def add_alert_type4():
    # Add alert type 4
    email = session.get('email', None)
    user = UserInterface(email)
    coin = request.form.get('coin')
    minutes = request.form['minutes'].replace(',', '')  # remove commas
    if coin == 'Select Cryptocurrency':  # If they have not selected a coin
        flash('Please select a coin', 'danger')
    elif not minutes.replace('.', '').isdigit():  # If they have not entered a valid number of minutes
        flash('Please enter a valid number of minutes', 'danger')
    elif float(minutes) > 1000000:  # If the number of minutes is too big
        flash('Enter a number of minutes less than 1 million', 'danger')
    else:
        alertID = user.add_alert_type4(coin, float(minutes))
        alert = AlertMonitor(alertID)
        executor.submit(alert.monitor_alert)
        flash('The alert has been added successfully!', 'success')
    return redirect('/addAlerts')


if __name__ == "__main__":
    myapp.run(debug=True)
