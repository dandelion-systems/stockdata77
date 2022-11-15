#!/usr/bin/env python3

# This is a demo code for Stocks class implemented
# in stockquotes module
#
# Copyright 2022 Dandelion Systems FZ LLC <dandelion.systems@gmail.com>

from time import sleep
from stockquotes import Stocks

# Create a database of stock quotes and fill it up
stocks = Stocks()
stocks.append("AAPL")
stocks.append("U")
stocks.append("MSFT")

# Start updating the quotes at 2 second intervals
stocks.maintain(2)

# Print the updated quotes every 2 seconds.
# Replace U wth GOOGL at some point.
# To see the changes in quotes between the 
# printouts run this code during trading hours 
# in New York
for i in range(4):
	sleep(2)
	if i == 2: 
		stocks.remove("U")
		stocks.append("GOOGL")
	print(stocks)

# Stop updating the quotes
stocks.desist()

# Get the latest quote for a specific symbol,
# MSFT in this case
key = stocks.makeKey("MSFT")
if key in stocks:
	print("Stock quote for MSFT")
	print("Name   = " + stocks.getCompanyName(key))
	print("Price  = {0:.2f}".format(stocks.getPrice(key)))
	print("Change = {0:.2f}%".format(stocks.getPriceChng(key)*100))
