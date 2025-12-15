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

	Currently supported stock APIs are FMP, ALPHA VANTAGE (AV) and MOEX / MOEXBONDS.
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

	__sx_list = ("FMP", "AV", "MOEX", "MOEXBONDS")	# Valid API providers
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
		result =  "TICKER".ljust(20," ") + "NAME".ljust(20, " ") + "PRICE".ljust(9, " ") + "CHANGE".ljust(10, " ") + "API".ljust(10, " ") + os.linesep
		result +=       "".ljust(19,"-") +    " ".ljust(20, "-") +     " ".ljust(9, "-") +      " ".ljust(10, "-") +   " ".ljust(10, "-") + os.linesep

		for key in self.__stocks.keys():
			truncatedKey = key.split(self.__delimiter)[0]
			if len(truncatedKey) > 19: truncatedKey = truncatedKey[:16] + "..."
			truncatedName = self.getCompanyName(key)
			if len(truncatedName) > 19: truncatedName = truncatedName[:16] + "..."
			truncatedAPI = API = key.split(self.__delimiter)[1]
			if len(truncatedAPI) > 9: truncatedAPI = truncatedAPI[:6] + "..."

			result += truncatedKey.ljust(20," ") + truncatedName.ljust(20, " ") 
			if API == "MOEXBONDS":
				result += "{0:7.2f}% {1:8.2f}% ".format(100*self.getPrice(key), 100*self.getPriceChng(key))
			else:
				result += "{0:8.2f} {1:8.2f}% ".format(self.getPrice(key), 100*self.getPriceChng(key))
			result += truncatedAPI.ljust(8," ") + os.linesep
		
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
					res = self.__request("financialmodelingprep.com", "/stable/quote?symbol=" + ticker + "&apikey=" + api_key)

					json_obj = loads(res)
					json_result = json_obj[0]
					if json_result is not None:
						company = json_result['name']
						price = float(json_result['price'])
						changePercent = float(json_result['changePercentage']) / 100

				case "AV":
					res = self.__request("www.alphavantage.co", "/query?function=GLOBAL_QUOTE&symbol=" + ticker + "&apikey=" + api_key)

					json_obj = loads(res)
					json_result = json_obj['Global Quote']
					if json_result is not None:
						company = json_result['01. symbol']
						price = float(json_result['05. price'])
						changePercent = float(json_result['10. change percent'][:-1]) / 100
			
				case "MOEX":
					# sample:
					# https://iss.moex.com/iss/engines/stock/markets/shares/securities/X5.xml
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
									api_price = entry.attrib["MARKETPRICE"] if entry.attrib["LAST"] == "" else entry.attrib["LAST"]
									price = float(api_price)
									changePercent = float(entry.attrib["LASTTOPREVPRICE"]) / 100.00
									is_found = True
									break
					if not is_found:
						key = None
			
				case "MOEXBONDS":
					# samples:
					# https://iss.moex.com/iss/engines/stock/markets/bonds/securities/SU26248RMFS3.xml
					# https://iss.moex.com/iss/engines/stock/markets/bonds/securities/RU000A106LL5.xml
					api_key = "" # discard API key for MOEXBONDS
					xml_result_str = self.__request("iss.moex.com", "/iss/engines/stock/markets/bonds/securities/" + ticker + ".xml")
					xml_result_tree = xmlet.fromstring(xml_result_str)

					is_found = False
					for dta in xml_result_tree.findall("data"):
						if dta.attrib["id"] == "securities":
							for entry in dta.find("rows").findall("row"):
								if entry.attrib["BOARDID"] in ("TQCB", "TQOB"):
									company = entry.attrib["SECNAME"]
									price = float(entry.attrib["PREVPRICE"]) / 100.0 # previous day's close
									break
						if dta.attrib["id"] == "marketdata":
							for entry in dta.find("rows").findall("row"):
								if entry.attrib["BOARDID"] in ("TQCB", "TQOB"):
									if entry.attrib["LAST"] != "":                   # this will be empty on a non trading day, in which case
										price = float(entry.attrib["LAST"]) / 100.00 # we have `price` assigned to previous day's close
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

