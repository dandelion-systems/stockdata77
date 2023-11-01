# Python interface to stock quotes providers

`stockdata77` provides `Stocks` class which facilitates interfacing with real-time information providers of securities trading data. Currently it supports APIs of Financial Modeling Prep, Alpha Vantage, Yahoo Finance and MOEX. Please note that FMP and AV providers will require an API key. It is designed primarily to be used with stock and ETF symbols, though FMP will also provide FOREX data.

## Usage summary

`Stocks` class creates and maintains a dictionary of traded securities quotes. Stored values are security long name, current price and change to previous close. The price is stored in the currency of the security for a nominal of 1. The change is stored as a fraction of the price, i.e. a change of 2% will be stored as 0.02.

Use `append(ticker, api)` method to fill it with individual stock quotes. 

Once you have all the quotes you need, you can use `Stocks[key]` to obtain trading data as a list of values. Alternatively, call individual `getXXXXXX()` methods to obtain various components of the list. Prior to calling any of these you can use the `in` operator to check if a `key` has a corresponding record.

The `key` is composed out of the stock ticker and the name of the API provider. `makeKey(ticker, api)` will 
get you the `key`. Or you can simply store the value returned by `append()` or `update()`. Use `splitKey()` to reverse `makeKey()`.

The instances of the `Stocks` class are iterable. Trying this code

	import stockdata77

	stocks = Stocks()
	stocks.append("AAPL")
	stocks.append("U")
	for entry in stocks:
		print(entry)

will print tuples of `(key, [name, price, change])` like this:

	('AAPL:YF', ['Apple Inc.', 155.74, 0.0755525])
	('U:YF', ['Unity Software Inc.', 29.23, 0.048421822])

Attempting to cast the whole instance to `str` type will get you a formatted table with the current quotes. For instance appending 

	print(stocks)

to the example above will get you this:

	TICKER      NAME                PRICE    CHANGE 
	----------- ------------------- -------- ---------
	AAPL:YF     Apple Inc.            155.74     7.56%
	U:YF        Unity Software ...     29.23     4.84%

Use `maintain(interval)` to fork a thread that updates the quotes at the given intervals in seconds. Invoking `desist()` will stop the updates. See the included `sample_cli.py` script for an example.

## `Stocks` class methods

> `Stocks` class does not expose any fields. Use the methods described below to obtain the necessary. In addition to these you can iterate through an instance of `Stocks`, read individual records by indexing it with a `key` (see `append()` for the explanation of keys), and cast it to `str` type which returns a formatted text table with full stored data.

`append(ticker:str, api:str, api_key:str = "", forceUpdate = False)` - appends the internal dictionary with the current trading data for the `ticker`. How close it is to real-time depends on the API provider and, in case you supply `api_key`, on your subscription plan. `ticker` must be a valid symbol like "AAPL", `api` must be one of "FMP, "AV", "YF" or "MOEX". The information is appended only in case the internal dictionary does not yet have an entry with the same key. Otherwise, it is neither appended nor updated, which allows skipping web API calls. To force the update set `forceUpdate` to `True`. It is mandatory to provide `api_key` if either "FMP" or "AV" is used.

Using `append()` is the way to fill up the `Stocks` instance initially. The tickers can come from a source that might contain duplicates and sticking with `forceUpdate = False` and thus skiping web API calls for duplicate tickers will optimise your code for speed and minimise the impact on the API providers.

The returned value is the `key` to the the internal dictionary for the record of this ticker/api pair. If the returned `key` is not stored in the calling code it can be constructed again by calling the `makeKey()` menthod. If either the supplied `ticker` or the `api` names are invalid, `append()` returns `None`.

`update(ticker:str, api:str, api_key:str = "")` - same as `append()` but with `forceUpdate` set to `True`.

`remove(ticker:str, api:str)` - removes the quote for the `ticker`. `ticker` and `api` are the same as when calling `append()`. If there is no entry for the ticker/api pair in the internal database, `remove()` returns silently.

`maintain(interval:int)` - start updating stock quotes at regular intervals (in seconds). This method forks a thread that keeps calling the relevant APIs and updating the internal dictionary with new data. Use `desist()` to stop.

`desist()` - stop updating stock quotes.

`makeKey(ticker:str, api:str)` - makes a `key` used in the internal dictionary maintained by `Stocks` to address the trading data records. Returns a `str` value of the `key`.

`splitKey(key:str)` - reverses `makeKey()` and returns a tuple of `(ticker, api)`.

`getCompanyName(key:str)` - obtains a long company name for the ticker used to make the `key`.

`getPrice(key:str)` - obtains a `float` value of the current price for the ticker used to make the `key`.

`getPriceChng(key:str)` - obtains  a `float` value of the current price change from previous close for the ticker used to make the `key`. The change is stored as a fraction of the price, i.e. a change of 2% will be stored as 0.02.

## Final notes

### Usage scenarios

> Note: As of October 2023 Yahoo Finance API was not operational. The examples below use "YF" simply to avoid using `api_key` paramater.

There are at least two scenarios the `Stocks` class was designed for.

#### Static
Add quotes with `append()` and then use them without updating. Sample code:
	
	#!/usr/bin/env python3

	from stockdata77 import Stocks

	stocks = Stocks()
	key = stocks.append("AAPL", "YF")

	if key is not None:
		print("Stock quote for AAPL")
		print("Name   = " + stocks.getCompanyName(key))
		print("Price  = {0:.2f}".format(stocks.getPrice(key)))
		print("Change = {0:.2f}%".format(stocks.getPriceChng(key)*100))
	else:
		print("Quote not found")

#### Dynamic
Add quotes with `append()` and then keep them alive to use in some dymnamic way like plotting real-time price graphs or directing business logic. The API provider and your subscription plan should allow real-time quotes of course. Sample code:

	#!/usr/bin/env python3
	
	from time import sleep
	from stockdata77 import Stocks

	stocks = Stocks()
	stocks.append("AAPL", "YF")
	stocks.append("U", "YF")
	stocks.append("MSFT", "YF")

	stocks.maintain(2) # start updating the quotes at 2 second intervals

	for i in range(4):
		sleep(2)       # wait for updates
		if i == 2:     # replace a symbol at some point for some reason
			stocks.remove("U", "YF")
			stocks.append("GOOGL", "YF")
		print(stocks)  # display updated quotes

	stocks.desist()    # stop updating the quotes

	print(stocks)

### Thread safety

> `Stocks` class _iterator is not thread-safe_.

Avoid iterating through an instance of `Stocks` class in more than one thread at a time. Use [barrier objects](https://docs.python.org/3/library/threading.html?highlight=barriers#barrier-objects) or other means of resource mutual exclusion to contol this in your code.

The methods of the `Stocks` class itself do not use the implemented iterator. For instance, `maintain()` or `__str__()` methods though iterating through the records in the internal dictionary, use other means for this. You can use these methods (almost) safely in your multi-threaded applications as long as you avoid `remove()`-ing. If you need to `remove()` a quote while `maintain()`-ing, call `desist()` first to pause the updates, then call `remove()` and invoke `maintain()` again.
