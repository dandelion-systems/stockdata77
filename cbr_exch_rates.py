#!/usr/bin/env python3

import os
import sys
from datetime import date
from datetime import timedelta
import xml.etree.ElementTree as xmlet
from http.client import HTTPConnection
from optparse import OptionParser

def get_all_rates(d:date) -> dict:
	"""
	get_all_rates(date_str) retrieves FX rate information
	from the Central Bank of Russian Federation for the date.
	
	See http://www.cbr.ru/development/sxml/ for more details.
	"""

	db = {}
	date_str = '{0:02}/{1:02}/{2:02}'.format(d.day, d.month, d.year)	# The date should be in the format 'DD/MM/YYYY'
	
	api = HTTPConnection("www.cbr.ru")
	api.request("GET", "/scripts/XML_daily.asp?date_req=" + date_str)
	xml_str = api.getresponse().read().decode('cp1251')
	xml_tree = xmlet.fromstring(xml_str)
	
	for currency in xml_tree.findall('Valute'):
		curr_charcode = currency.find('CharCode').text
		curr_name = currency.find('Name').text
		curr_erate_str = currency.find('Value').text
		curr_nominal = currency.find('Nominal').text
		curr_numcode = currency.find('NumCode').text

		curr_erate = float(curr_erate_str.replace(',', '.'))
		#					 0  1          2           3             4
		db[curr_charcode] = [d, curr_name, curr_erate, curr_nominal, curr_numcode]
	
	return db

def tabulate_rates(rates:dict) -> str:
	res_str = ''

	for curr_charcode in rates.keys():
		curr_name = rates[curr_charcode][0]
		curr_erate = rates[curr_charcode][1]
		curr_nominal = rates[curr_charcode][2]
		curr_numcode = rates[curr_charcode][3]
		res_str += curr_charcode + '\t' + curr_erate + ' руб\tза ' + curr_nominal + ' ' + curr_name + ' (код ' + curr_numcode + ')' + os.linesep

	return res_str

def average_annual_fx_rate(year:int, currency:str = 'USD', *, print_progress:bool = False) -> float:
	today = date.today()
	d = date(year, 1, 1)

	if d > today:
		raise ValueError()

	days_counter = 0
	fx_rate = 0.0
	month = 0

	while (True):
		if d > today:
			break

		if print_progress and d.month > month:
			month = d.month
			print(str(month), end='...')

		if d.isoweekday() not in [6, 7]:
			if (all_fx_rates := get_all_rates(d)) == {}:
				raise ValueError()
			if currency not in all_fx_rates:
				raise IndexError()
			days_counter += 1
			fx_rate += all_fx_rates[currency][2]

		d += timedelta(days=1)
		if d.year > year:
			break

	fx_rate /= days_counter

	return round(fx_rate,4)

def main():
	optParser = OptionParser(usage="Usage: %prog [options] YYYY-MM-DD | YYYY" + os.linesep + "See --help for options.")
	optParser.add_option("-c", "--currency", help="get rate for currency, default=USD", action="store", type='string', default='USD', dest='currency')

	try:
		(options,args) = optParser.parse_args(sys.argv)
		currency = options.currency
		currency = currency.upper()
		match len(args[1]):
			case 4:
				year_average = True
				YYYY = args[1]
			case 10:
				year_average = False
				iso_date = args[1]
			case _:
				optParser.print_help()
				raise ValueError
	except IndexError:				# handle unknown options as OptionParser does not
		optParser.print_help()		# print help by default in this case
		return
	except:							# if --help is specified, OptionParser prints help by defaut
		return						# and throws an exception. We handle it gracefully here

	if year_average:
		rate = average_annual_fx_rate(int(YYYY), currency)
		print(YYYY + ' ' + currency + '/RUB average = {0:.4f}'.format(rate))
	else:
		rate = get_all_rates(date.fromisoformat(iso_date))[currency][2]
		print(iso_date + ' ' + currency + '/RUB average = {0:.4f}'.format(rate))

	return

if __name__ == '__main__':
	main()
