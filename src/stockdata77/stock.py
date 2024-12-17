"""
	This file is part of stockdata77 Python module.

	Copyright 2022 Dandelion Systems <dandelion.systems@gmail.com>

	stockdata77 is free software; you can redistribute it and/or modify
	it under the terms of the MIT License.

	stockdata77 is distributed in the hope that it will be useful, but
	WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	See the MIT License for more details.

	SPDX-License-Identifier: MIT
"""

import os
from json import loads
import xml.etree.ElementTree as xmlet
from http.client import HTTPSConnection
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

	Currently supported stock APIs are FMP, ALPHA VANTAGE (AV), Yahoo Finance (YF) and MOEX.
	"""

	__stocks = {}
	"""
	__stocks dictionary holds the current stock quotes and other information.
	The current version has the following format:
	__stocks[key] = [Company_long_name:str, Current_price:float, Change_to_previous_close:float, API_key: str]

	Comments:
		Current_price is stored in the currency of the security for a nominal of 1
		Change_to_previous_close is stored as a fraction of the price, 
			i.e. the change of 2% will be stored as 0.02
	"""

	__sx_list = ("FMP", "AV", "YF", "MOEX")	# Valid API providers
	__delimiter = ":"						# Delimiter for __stocks dictionary key, the format is TICKER:API, e.g. AAPL:FMP

	__maintaining = False
	__daemon = None

	def __init__(self):
		return

	def makeKey(self, ticker:str, api:str):
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
	
	def __request(self, address:str, query:str):
		conn = HTTPSConnection(address)
		conn.request("GET", query)
		res = conn.getresponse()
		return res.read().decode('utf-8')

	def append(self, ticker:str, api:str, api_key:str = "", force_update = False):
		"""
		append() appends the dictionary __stocks with the current quote 
		for the ticker. 

		ticker must be a valid symbol like "AAPL".
		api must be one of __sx_list[] values.
		
		The information is appended only in case __stocks[] does not yet 
		have an entry with the same key. Otherwise, it is neither appended 
		nor updated, which allows to skip web API calls. To force the 
		update set force_update to True.

		The returned value is the key to the corresponding record 
		in __stocks[]. If the key is not stored in the calling code it
		can be constructed again by calling the makeKey() menthod.
		"""
		
		if ticker is None: ticker = ""
		ticker = ticker.upper()
		if api is None: api = ""
		api = api.upper()
		if api_key is None: api_key = ""

		if ticker == "" or api not in self.__sx_list:
			return None

		key = self.makeKey(ticker, api)

		if key in self.__stocks and not force_update:
			return key

		company = ""
		price = 0.00
		changePercent = 0.00

		try:

			match api:
				case "FMP":
					res = self.__request("financialmodelingprep.com", "/api/v3/quote-order/" + ticker + "?apikey=" + api_key)

					json_obj = loads(res)
					json_result = json_obj[0]
					if json_result is not None:
						company = json_result['name']
						price = float(json_result['price'])
						changePercent = float(json_result['changesPercentage']) / 100

				case "AV":
					res = self.__request("www.alphavantage.co", "/query?function=GLOBAL_QUOTE&symbol=" + ticker + "&apikey=" + api_key)

					json_obj = loads(res)
					json_result = json_obj['Global Quote']
					if json_result is not None:
						company = json_result['01. symbol']
						price = float(json_result['05. price'])
						changePercent = float(json_result['10. change percent'][:-1]) / 100

				case "YF":	
					api_key = "" # discard API key for YF
					res = self.__request("query2.finance.yahoo.com", "/v6/finance/quoteSummary/" + ticker + "?modules=price")	

					json_obj = loads(res)
					json_result = json_obj['quoteSummary']['result']
					if json_result is not None:
						stockPriceInfo = json_result[0]['price']
						if stockPriceInfo['longName'] is not None: company = stockPriceInfo['longName']
						price = float(stockPriceInfo['regularMarketPrice']['raw'])
						changePercent = float(stockPriceInfo['regularMarketChangePercent']['raw'])
			
				case "MOEX":
					api_key = "" # discard API key for MOEX
					xml_result_str = self.__request("iss.moex.com", "/iss/engines/stock/markets/shares/securities/" + ticker + ".xml")
					xml_result_tree = xmlet.fromstring(xml_result_str)

					is_found = False
					for dta in xml_result_tree.findall("data"):
						if dta.attrib["id"] == "securities":
							for entry in dta.find("rows").findall("row"):
								if entry.attrib["BOARDID"] == "TQBR":
									company = entry.attrib["SECNAME"]
									break
						if dta.attrib["id"] == "marketdata":
							for entry in dta.find("rows").findall("row"):
								if entry.attrib["BOARDID"] == "TQBR":
									price = float(entry.attrib["LAST"])
									changePercent = float(entry.attrib["LASTTOPREVPRICE"]) / 100.00
									is_found = True
									break
					if not is_found:
						key = None
		except:
			key = None		
		
		if key is not None:
			self.__stocks[key] = [company, price, changePercent, api_key]

		return key
		
	def update(self, ticker:str, api:str, api_key:str = ""):
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

		return self.append(ticker=ticker, api=api, api_key=api_key, force_update=True)

	def remove(self, ticker:str, api:str):
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
				api_key = self[key][3]
				self.update(ticker=ticker, api=api, api_key=api_key)

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

