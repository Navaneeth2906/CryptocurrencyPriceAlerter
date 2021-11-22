from AlertMonitor import *
from PriceMonitor import *
from UserInterface import *
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
        time.sleep(10)


executor = concurrent.futures.ThreadPoolExecutor()
f1 = executor.submit(all_prices_check)

