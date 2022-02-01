import sqlite3, random, datetime, bs4, requests
from PriceMonitor import *
from bs4 import BeautifulSoup


class UserInterface():

    def __init__(self, email):
        self.email = email

    def display_alerts(self):
        # Retrieve all the IDs and messages of the alerts and return them
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        c.execute('''SELECT TPAID, Message FROM TPA WHERE Email = ? ''', (self.email,))
        tpaMs = c.fetchall()
        c.execute('''SELECT SPAID, Message FROM SPA WHERE Email = ? ''', (self.email,))
        spaMs = c.fetchall()
        db.close()
        ids = []  # One list for the IDs
        messages = []  # And another for the messages
        for line in tpaMs:
            ids.append(line[0])
            messages.append(f'Alert me when {line[1]}')
        for line in spaMs:
            ids.append(line[0])
            messages.append(f'Alert me when {line[1]}')
        return ids, messages

    def add_alert_type1(self, coin, price):
        # First create a unique ID
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        c.execute('''SELECT TPAID FROM TPA''')
        tpaIDs = c.fetchall()
        done = False
        while not done:
            tpaID = '1' + coin[0:1] + str(price)[0:1] + self.email[0:1] + str(random.randint(0, 9)) + str(
                random.randint(0, 9))
            if tpaID not in tpaIDs:
                done = True
        # Now create an appropriate message
        message = f'the price of {coin} has reached ${price}.'
        # Now add everything to the database
        c.execute('''INSERT INTO TPA VALUES (?, ?, ?, ?, ?) ''', (tpaID, coin, price, message, self.email))
        db.commit()
        db.close()
        return tpaID

    def add_alert_type2(self, coin, increasedOrDecreased, percentage):
        # First find the target price
        db = sqlite3.Connection("Prices.db")
        c = db.cursor()
        c.execute('''SELECT Price FROM CurrentPrice WHERE Cryptocurrency = ? ''', (coin,))
        price = c.fetchall()[0][0]
        db.close()
        if increasedOrDecreased == "increased":
            price += price * (percentage / 100)
        elif increasedOrDecreased == "decreased":
            price -= price * (percentage / 100)
        # Now create a unique ID
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        c.execute('''SELECT TPAID FROM TPA''')
        tpaIDs = c.fetchall()
        done = False
        while not done:
            tpaID = '2' + coin[0:1] + str(percentage)[0:1] + self.email[0:1] + str(random.randint(0, 9)) + str(
                random.randint(0, 9))
            if tpaID not in tpaIDs:
                done = True
        # Now create the message
        message = f'the price of {coin} has {increasedOrDecreased} by {percentage}% from the price on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.'
        # Now add everything to the database
        c.execute('''INSERT INTO TPA VALUES (?, ?, ?, ?, ?) ''', (tpaID, coin, price, message, self.email))
        db.commit()
        db.close()
        return tpaID

    '''
    # Screen scraping with Digital Coin
    @staticmethod
    def highest_or_lowest(coin, daysAgo, highestOrLowest):  # Input currency and the number of days ago you want the price for
        coins = {'BTC': 'bitcoin', 'ETH': 'ethereum', 'DOGE': 'dogecoin', 'LTC': 'litecoin'}
        coin = coins[coin]
        highList = []
        lowList = []
        r = requests.get(
            'https://digitalcoinprice.com/coins/' + coin + '/historical-data/30-days')  # Get the correct website
        soup = bs4.BeautifulSoup(r.text, "lxml")  # Get the HTMl
        c = soup.find_all('td', {'class': "text-center"})  # Extract the data from the needed table
        for i in range(0, len(c), 8):  # Loop through data
            if '\n' in c[i].text:  # Stop at unnecessary characters
                break
            else:
                highList.append(c[i + 3].text)
                lowList.append(c[i + 4].text)
            if len(highList) == daysAgo:  # Stop at the correct number of days ago
                break
        # Return the needed value
        if highestOrLowest == "highest":
            return max(highList)
        elif highestOrLowest == "lowest":
            return min(lowList)
    '''

    # Screen scraping from investing.com
    @staticmethod
    def highest_or_lowest(coin, daysAgo, highestOrLowest):  # Input currency and the number of days ago you want the price for
        coins = {'BTC': 'bitcoin', 'ETH': 'ethereum', 'DOGE': 'dogecoin', 'LTC': 'litecoin'}
        coin = coins[coin]
        highList = []
        lowList = []
        # Specify a header to bypass the error
        hdr = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        r = requests.get(f'https://uk.investing.com/crypto/{coin}/historical-data',
                         headers=hdr)  # Get the correct website
        soup = bs4.BeautifulSoup(r.text, "lxml")  # Get the HTMl
        c = soup.find_all('tr')
        # Remove unecessary data
        c = c[1:len(c) - 1]
        for i in range(daysAgo + 1):
            highList.append(c[i].text.split()[5].replace(',', ''))
            lowList.append(c[i].text.split()[6].replace(',', ''))
        # Return the needed value
        if highestOrLowest == "highest":
            return max(highList)
        elif highestOrLowest == "lowest":
            return min(lowList)

    def add_alert_type3(self, coin, daysAgo, highestOrLowest):
        # First find the target price
        price = self.highest_or_lowest(coin, daysAgo, highestOrLowest)
        # Now create a unique ID
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        c.execute('''SELECT TPAID FROM TPA''')
        tpaIDs = c.fetchall()
        done = False
        while not done:
            tpaID = '3' + coin[0:1] + str(daysAgo)[0:1] + self.email[0:1] + str(random.randint(0, 9)) + str(
                random.randint(0, 9))
            if tpaID not in tpaIDs:
                done = True
        # Now create the message
        message = f'the price of {coin} has reached the {highestOrLowest} price from {daysAgo} days before {datetime.datetime.now().strftime("%Y-%m-%d")}.'
        # Now add everything to the database
        c.execute('''INSERT INTO TPA VALUES (?, ?, ?, ?, ?) ''', (tpaID, coin, price, message, self.email))
        db.commit()
        db.close()
        return tpaID

    def add_alert_type4(self, coin, minutes):
        # Create a unique ID
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        c.execute('''SELECT SPAID FROM SPA''')
        spaIDs = c.fetchall()
        done = False
        while not done:
            spaID = '4' + coin[0:1] + str(minutes)[0:1] + self.email[0:1] + str(random.randint(0, 9)) + str(
                random.randint(0, 9))
            if spaID not in spaIDs:
                done = True
        # Create the message
        message = f'the price of {coin} has remained stagnant for {minutes} minutes.'
        # Now add to the database
        c.execute('''INSERT INTO SPA VALUES (?, ?, ?, ?, ?) ''', (spaID, coin, minutes, message, self.email))
        db.commit()
        db.close()
        return spaID


def display_prices():
    # Return all the prices of the cryptocurrencies
    db = sqlite3.Connection("Prices.db")
    c = db.cursor()
    c.execute('''SELECT * FROM CurrentPrice''')
    priceData = c.fetchall()
    db.close()
    display = []
    for record in priceData:
        display.append(record[0] + ': $' + str(record[1]))
    return display


def delete_alert(alertID):
    # Delete the alert from the correct table
    db = sqlite3.Connection("UsersAndAlerts.db")
    c = db.cursor()
    if alertID[0:1] == '4':
        c.execute('''DELETE FROM SPA WHERE SPAID = ? ''', (alertID,))
    else:
        c.execute('''DELETE FROM TPA WHERE TPAID = ? ''', (alertID,))
    db.commit()
    db.close()


def login(email, password):
    db = sqlite3.Connection("UsersAndAlerts.db")
    c = db.cursor()
    # Retrieve a matching username and password pair from the table
    c.execute('''SELECT Email, Password FROM Users WHERE Email = ? AND Password = ? ''', (email, password))
    rows = c.fetchall()
    db.close()
    if len(rows) != 0:  # If the details are correct, take them to the next page
        return False, None
    else:
        return True, 'You have provided the incorrect details!'


def register(demail, dpassword):
    if '@' not in demail[1:]:  # Check if email is valid
        return True, 'You have entered an invalid email!'
    elif len(dpassword) > 15 or len(dpassword) < 8:  # Check if password is valid
        return True, 'Your password must be between 8 and 15 characters!'
    else:
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        # Check if there is already an account with this email
        c.execute('''SELECT Email FROM Users WHERE Email = ? ''', (demail,))
        rows = c.fetchall()
        if len(rows) == 0:
            # Insert values into the table
            c.execute('''INSERT INTO Users VALUES (?, ?)''', (demail, dpassword))
            db.commit()
            db.close()
            # Take them to the next page
            return False, None
        else:
            db.close()
            return True, 'This email is already registered!'
