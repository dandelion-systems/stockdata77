# This is a demo code for Stocks class implemented
# in stockquotes module
#
# Copyright 2022 Dandelion Systems <dandelion.systems@gmail.com>
#
# SPDX-License-Identifier: MIT

from time import sleep
from stockdata77 import Stocks

# Create a database of stock quotes and fill it up
stocks = Stocks()
stocks.append("TSLA", api="FMP", api_key="YOUR_FMP_API_KEY_HERE")
stocks.append("NVDA", api="AV", api_key="YOUR_AV_API_KEY_HERE")
stocks.append("SBER", "MOEX")

print(stocks)

# Start updating the quotes at 2 second intervals
stocks.maintain(2)

for i in range(10):
	sleep(2)
	print(stocks)

# Stop updating the quotes
stocks.desist()
