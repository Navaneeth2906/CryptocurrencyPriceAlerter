from UserInterface import *
import smtplib
import time
from email.message import EmailMessage


class AlertMonitor():

    def __init__(self, alertID):
        self.alertID = alertID

    def delete_alert(self):
        # Delete the alert from the correct table
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        if self.alertID[0:1] == '4':
            c.execute('''DELETE FROM SPA WHERE SPAID = ? ''', (self.alertID,))
        else:
            c.execute('''DELETE FROM TPA WHERE TPAID = ? ''', (self.alertID,))
        db.commit()
        db.close()

    @staticmethod
    def email_alert(message, to):
        # First create the message
        msg = EmailMessage()
        msg.set_content(message)  # Add content
        msg['subject'] = 'Cryptocurrency Price Alert!'  # Add subject
        msg['to'] = to  # Add recipient email

        # Add sender details
        user = "cryptocurrncy29@gmail.com"
        msg["from"] = user
        password = "budsglnjbtxewjza"

        # Send the email using SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

        server.quit()


    def monitor_tpa(self, row):
        db = sqlite3.Connection("Prices.db")
        c = db.cursor()
        c.execute('''SELECT Price FROM CurrentPrice WHERE Cryptocurrency = ?''', (row[1],))
        price = c.fetchall()[0][0]
        db.close()
        if (price <= row[2] and row[3] == 'less') or (price >= row[2] and row[3] == 'greater'):
            try:
                self.email_alert(f'Alert: {row[4]} The price is now ${price}.', row[5])  # Send email
                print(f'To {row[5]} sent "Alert: {row[4]}" The price is now ${price}.')
            except:  # If there is an error sending the email
                print(f"Email to {row[5]} with message 'Alert: {row[4]} The price is now ${price}.' failed to send.")
            self.delete_alert()



    def monitor_spa(self):
        # Retrieve alert data
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        c.execute('''SELECT * FROM SPA WHERE SPAID = ?''', (self.alertID,))
        spa = c.fetchall()
        db.close()
        # Retrieve price
        db = sqlite3.Connection("Prices.db")
        c = db.cursor()
        c.execute('''SELECT Price FROM CurrentPrice WHERE Cryptocurrency = ?''', (spa[0][1],))
        oldPrice = c.fetchall()[0][0]
        db.close()
        # Set time counter
        timeStagnant = 0
        while True:
            time.sleep(10)
            # Find new price
            db = sqlite3.Connection("Prices.db")
            c = db.cursor()
            c.execute('''SELECT Price FROM CurrentPrice WHERE Cryptocurrency = ?''', (spa[0][1],))
            newPrice = c.fetchall()[0][0]
            db.close()
            # Check if price has changed
            if oldPrice <= (newPrice * 1.001) and oldPrice >= (newPrice * 0.999):  # within +/- 0.01%
                timeStagnant += 10
            else:
                oldPrice = newPrice
                timeStagnant = 0
            # Check if limit has been reached
            if (timeStagnant / 60) >= spa[0][2]:
                try:
                    self.email_alert(f"Alert: {spa[0][3]}", spa[0][4])  # Send email
                    print(f'To {spa[0][4]} sent "Alert: {spa[0][3]}"')
                except:  # If there is an error sending the email
                    print(f"Email to {spa[0][4]} with message 'Alert: {spa[0][3]}' failed to send.")
                timeStagnant = 0  # Reset counter
                self.delete_alert()

            # Check if this alert has been deleted
            db = sqlite3.Connection("UsersAndAlerts.db")
            c = db.cursor()
            c.execute('''SELECT * FROM SPA WHERE SPAID = ?''', (self.alertID,))
            spa = c.fetchall()
            db.close()
            if len(spa) == 0:
                break

    def monitor_alert(self):
        if self.alertID[0:1] == '4':
            self.monitor_spa()
        else:
            self.monitor_tpa()

