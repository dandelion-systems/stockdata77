"""
	This file is part of stockquotes Python module.

	Copyright 2022 Dandelion Systems FZ LLC <dandelion.systems@gmail.com>

	stockquotes is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	stockquotes is distributed in the hope that it will be useful, but
	WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with stockquotes. If not, see <http://www.gnu.org/licenses/>.
"""

import os
from json import loads
import xml.etree.ElementTree as xmlet
from http.client import HTTPSConnection
from http.client import RemoteDisconnected
from threading import Thread
from time import sleep

class Stocks:
	"""
	Class Stocks creates and maintains a dictionary of stock quotes.

	Call Stocks.append() to fill it with individual stock quotes. 
	Once you have all the quotes you need, you can use Stocks[key] 
	to obtain stock information as a list of values. Alternatively,
	call individual getXXXXXX(key) methods to obtain various 
	components of the list.

	Currently supported stock APIs are YF and MOEX.
	"""

	__apiConnYF = None
	"""
	__apiConnYF is a connection point for Yahoo Finance API. 
	The YF API request will look like this:
	https://query2.finance.yahoo.com/v10/finance/quoteSummary/TICKER?modules=price
	"""
	
	__apiConnMOEX = None
	"""
	__apiConnMOEX is a connection point for MOEX API. 
	The MOEX API request will look like this:
	https://iss.moex.com/iss/engines/stock/markets/shares/securities/TICKER.xml
	"""

	__stocks = {}
	"""
	__stocks dictionary holds the current stock quotes and other information.
	The current version has the following format:
	__stocks[key] = [Company_long_name:str, Current_price:float, Change_to_previous_close:float]

	Comments:
		Current_price is stored in the currency of the security for a nominal of 1
		Change_to_previous_close is stored as a fraction of the price, 
			i.e. the change of 2% will be stored as 0.02
	"""

	__sx_list = ("YF", "MOEX")
	__delimiter = ":"

	__maintaining = False
	__daemon = None

	def __init__(self):
		self.__apiConnYF = HTTPSConnection("query2.finance.yahoo.com")
		self.__apiConnMOEX = HTTPSConnection("iss.moex.com")

	def makeKey(self, ticker:str, api:str = "YF"):
		return ticker + self.__delimiter + api

	def splitKey(self, key:str):
		return key.split(self.__delimiter)

	def getCompanyName(self, key:str):
		return self.__stocks[key][0]

	def getPrice(self, key:str):
		return self.__stocks[key][1]

	def getPriceChng(self, key:str):
		return self.__stocks[key][2]

	def __getitem__(self, key:str):
		return self.__stocks[key]

	def __iter__(self):
		self.__maxCount = len(self.__stocks)
		self.__iterCount = 0
		self.__valuesList = list(self.__stocks.items())
		return self

	def __next__(self):
		if self.__iterCount < self.__maxCount:
			self.__iterCount += 1
			return self.__valuesList[self.__iterCount-1]
		else:
			raise StopIteration

	def __str__(self):
		result =  "TICKER".ljust(12," ") + "NAME".ljust(20, " ") + "PRICE".ljust(8, " ") + " CHANGE".ljust( 8, " ") + os.linesep
		result +=       "".ljust(11,"-") +    " ".ljust(20, "-") +     " ".ljust(9, "-") +       " ".ljust(10, "-") + os.linesep

		for key in self.__stocks.keys():
			trucatedName = self.getCompanyName(key)
			if len(trucatedName) > 15: trucatedName = trucatedName[:15] + "..."

			result += key.ljust(12," ") + trucatedName.ljust(20, " ") 
			result += "{0:8.2f} {1:8.2f}%".format(self.getPrice(key), 100*self.getPriceChng(key)) + os.linesep
		
		return result

	def __contains__(self, key:str):
		return key in self.__stocks

	def append(self, ticker:str, api:str = "YF", forceUpdate = False):
		"""
		append() appends the dictionary __stocks with the current quote 
		for the ticker. 

		ticker must be a valid symbol like "AAPL".
		api must be one of __sx_list[] values.
		
		The information is appended only in case __stocks[] does not yet 
		have an entry with the same key. Otherwise, it is neither appended 
		nor updated, which allows to skip web API calls. To force the 
		update set forceUpdate to True.

		The returned value is the key to the corresponding record 
		in __stocks[]. If the key is not stored in the calling code it
		can be constructed again by calling the makeKey() menthod.
		"""
		
		if ticker is None: ticker = ""
		ticker = ticker.upper()
		if api is None: api = ""
		api = api.upper()

		if ticker == "" or api not in self.__sx_list:
			return None

		key = self.makeKey(ticker, api)

		if key in self.__stocks and not forceUpdate:
			return key

		company = "Error: " + ticker + " not found at " + api
		price = 0.00
		changePercent = 0.00

		match api:
			case "YF":			
				self.__apiConnYF.request("GET", "/v10/finance/quoteSummary/" + ticker + "?modules=price")
				try:
					res = self.__apiConnYF.getresponse()
				except RemoteDisconnected:	# retry once in case the calling code was slow and the API provider dropped the connection
					self.__apiConnYF = HTTPSConnection("query2.finance.yahoo.com")
					self.__apiConnYF.request("GET", "/v10/finance/quoteSummary/" + ticker + "?modules=price")
					res = self.__apiConnYF.getresponse()

				try:
					jsonObj = loads(res.read().decode('utf-8'))
					jsonResult = jsonObj['quoteSummary']['result']
					if jsonResult is not None:
						stockPriceInfo = jsonResult[0]['price']
						if stockPriceInfo['longName'] is not None: company = stockPriceInfo['longName']
						price = float(stockPriceInfo['regularMarketPrice']['raw'])
						changePercent = float(stockPriceInfo['regularMarketChangePercent']['raw'])
				except:
					key = None
		
			case "MOEX":
				self.__apiConnMOEX.request("GET", "/iss/engines/stock/markets/shares/securities/" + ticker + ".xml")
				try:
					res = self.__apiConnMOEX.getresponse()
				except RemoteDisconnected:	# retry once in case the calling code was slow and the API provider dropped the connection
					self.__apiConnMOEX = HTTPSConnection("iss.moex.com")
					self.__apiConnMOEX.request("GET", "/iss/engines/stock/markets/shares/securities/" + ticker + ".xml")
					res = self.__apiConnMOEX.getresponse()

				xmlResultStr = res.read().decode('utf-8')
				xmlResultTree = xmlet.fromstring(xmlResultStr)

				for dta in xmlResultTree.findall("data"):
					if dta.attrib["id"] == "securities":
						for entry in dta.find("rows").findall("row"):
							if entry.attrib["BOARDID"] == "TQBR":
								try: 
									company = entry.attrib["SECNAME"]
								except:
									key = None
								break
					if dta.attrib["id"] == "marketdata":
						for entry in dta.find("rows").findall("row"):
							if entry.attrib["BOARDID"] == "TQBR":
								try: 
									price = float(entry.attrib["LAST"])
									changePercent = float(entry.attrib["LASTTOPREVPRICE"]) / 100.00
								except: 
									key = None
								break
				
		if key is not None:
			self.__stocks[key] = [company, price, changePercent]

		return key
		
	def update(self, ticker:str, api:str = "YF"):
		"""
		update() appends or updates __stocks[] with 
		the current quote for the ticker. 

		ticker must a valid security symbol like "AAPL".
		api must be one of __sx_list[] values.
		
		If __stocks[] does not yet have an entry with the same key it is
		appended. Otherwise, it is updated.

		The returned value is the key to the __stocks dictionary under which the
		information is stored. If the key is not stored in the calling code it
		can be constructed again by calling the makeKey() menthod.
		"""

		return self.append(ticker=ticker, api=api, forceUpdate=True)

	def remove(self, ticker:str, api:str = "YF"):
		"""
		remove() removes the quote for the ticker. 

		ticker must a valid security symbol like "AAPL".
		api must be one of __sx_list[] values.
		
		If there is no entry for the ticker/api pair in the 
		database, remove() returns silently.
		"""
		key = self.makeKey(ticker, api)
		if key in self.__stocks:
			del self.__stocks[key]

	def __updateWorker(self, interval:int):
		while self.__maintaining:
			sleep(interval)
			for key in self.__stocks.keys():
				(ticker, api) = self.splitKey(key)
				self.update(ticker=ticker, api=api)

	def maintain(self, interval:int):
		"""
		Start updating stock quotes at regular intervals (in seconds).
		Use desist() to stop.
		"""
		if not self.__maintaining:
			self.__maintaining = True
			self.__daemon = Thread(target=self.__updateWorker, args=(interval,), daemon=True)
			self.__daemon.start()

	def desist(self):
		"""
		Stop updating stock quotes at regular intervals (in seconds).
		"""
		self.__maintaining = False

