from AlertMonitor import *
import concurrent.futures



def all_prices_check():
    bitcoin = PriceMonitor('BTC')
    ethereum = PriceMonitor('ETH')
    litecoin = PriceMonitor('LTC')
    dogecoin = PriceMonitor('DOGE')
    while True:
        bitcoin.update_price()
        ethereum.update_price()
        litecoin.update_price()
        dogecoin.update_price()
        db = sqlite3.Connection("UsersAndAlerts.db")
        c = db.cursor()
        c.execute('''SELECT * FROM TPA''')
        tpa = c.fetchall()
        db.close()
        for row in tpa:
            alert = AlertMonitor(row[0])
            alert.monitor_tpa(row)
        time.sleep(10)



executor = concurrent.futures.ThreadPoolExecutor()
executor.submit(all_prices_check)




