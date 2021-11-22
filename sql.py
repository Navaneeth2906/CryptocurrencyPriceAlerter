import sqlite3

db = sqlite3.connect('UsersAndAlerts.db')
c = db.cursor()
# Create table for users
c.execute('''CREATE TABLE Users (Email text, Password text)''')
# Create table for stagnant price alerts
c.execute('''CREATE TABLE SPA (
SPAID text, 
Cryptocurrency text, 
MinutesStagnant real, 
Message text, 
Email text)''')
# Create table for target price alerts
c.execute('''CREATE TABLE TPA (
TPAID text, 
Cryptocurrency text, 
TargetPrice real, 
Message text, 
Email text)''')
db.commit()
db.close()

db = sqlite3.connect('Prices.db')
c = db.cursor()
# Create table to store current prices
c.execute('''CREATE TABLE CurrentPrice (Cryptocurrency text, Price real)''')
c.execute('''INSERT INTO CurrentPrice Values (?, ?) ''', ('BTC', 0))
c.execute('''INSERT INTO CurrentPrice Values (?, ?) ''', ('ETH', 0))
c.execute('''INSERT INTO CurrentPrice Values (?, ?) ''', ('DOGE', 0))
c.execute('''INSERT INTO CurrentPrice Values (?, ?) ''', ('LTC', 0))
db.commit()
db.close()
