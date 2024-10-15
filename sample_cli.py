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
stocks.append("SQQQ", api="FMP", api_key="YOUR_API_KEY_HERE")
stocks.append("AMZN", api="AV", api_key="YOUR_API_KEY_HERE")
stocks.append("GMKN", "MOEX")

# Start updating the quotes at 2 second intervals
stocks.maintain(2)

for i in range(2):
	sleep(2)

# Stop updating the quotes
stocks.desist()

print(stocks)
