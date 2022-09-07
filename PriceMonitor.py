import sqlite3, requests

class PriceMonitor():

    def __init__(self, name):
        self.name = name

    def update_price(self):
        # Retrieve the stored price
        db = sqlite3.connect('Prices.db')
        c = db.cursor()
        c.execute('''SELECT Price FROM CurrentPrice WHERE Cryptocurrency = ? ''', (self.name,))
        storedPrice = c.fetchall()
        db.close()
        # Retrieve the current price
        response = requests.get('https://api.coinbase.com/v2/prices/' + self.name + '-USD/spot')  # Get data
        data = response.json()  # Make dictionary
        currentPrice = float(data["data"]["amount"])
        if currentPrice != storedPrice:
            db = sqlite3.connect('Prices.db')
            c = db.cursor()
            c.execute('''UPDATE CurrentPrice SET Price = ? WHERE Cryptocurrency = ? ''',(currentPrice, self.name,))
            db.commit()
            db.close()




