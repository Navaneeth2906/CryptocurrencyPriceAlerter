import smtplib
from email.message import EmailMessage
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
email_alert('code works', 'navaneethmv7@gmail.com')
