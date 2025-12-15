# This is a demo code for Stocks class implemented
# in stockquotes module
#
# Copyright 2022 Dandelion Systems <dandelion.systems@gmail.com>
#
# SPDX-License-Identifier: MIT

from time import sleep
from stockdata77 import Stocks

stocks = Stocks() # create a database of stock quotes and fill it up
stocks.append("AAPL", "AV", "KEY")
stocks.append("U", "AV", "KEY")
stocks.append("MSFT", "AV", "KEY")

print(stocks)

stocks.maintain(2) # start updating the quotes at 2 second intervals

for i in range(4):
	sleep(2)       # wait for updates
	print(stocks)  # display updated quotes

stocks.desist()    # stop updating the quotes

