
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import datetime


def get_data(date):

  """
  :param date: datetime object
  :return: data dictionary of currency values.
  """

  # Prepare the URL
  yearMonth = date.strftime("%Y%m")
  dayMonthYear = date.strftime("%d%m%Y")
  url = f"https://www.tcmb.gov.tr/kurlar/{yearMonth}/{dayMonthYear}.xml"
  # Container for the date
  data_dict = {}

  # TODO Part 3
  try:
    tree = ET.parse(urlopen(url))
  except:
    print("HTTP Error 404: Not Found -", url)
    return data_dict
  root = tree.getroot()
  
  for currency in root.findall('Currency'):

    code = currency.get('CurrencyCode')

    # Skip it since this is not a currency.
    if code == "XDR":
        continue

    # TODO Part 2
    unit = float(currency.find('Unit').text)
    buying = float(currency.find('ForexBuying').text) * unit
    selling = float(currency.find('ForexSelling').text) * unit
    

    # Prepare a dictionary to store parsed information.
    cur_dict = {'buying': buying, 'selling': selling}

    # Save the currency dictionary to data dictionary.
    data_dict[code] = cur_dict

  # TODO Part 3
  return data_dict

# if __name__ == "__main__":
#   d1 = dict({'USD': {'buying': 6.9543, 'selling': 6.9668}, 'AUD': {'buying': 4.463, 'selling': 4.4921},
#              'DKK': {'buying': 1.0058, 'selling': 1.0107}, 'EUR': {'buying': 7.5122, 'selling': 7.5257},
#              'GBP': {'buying': 8.4708, 'selling': 8.5149}, 'CHF': {'buying': 7.1281, 'selling': 7.1739},
#              'SEK': {'buying': 0.7031, 'selling': 0.71038}, 'CAD': {'buying': 4.9269, 'selling': 4.9491},
#              'KWD': {'buying': 22.3556, 'selling': 22.6481}, 'NOK': {'buying': 0.6799, 'selling': 0.68447},
#              'SAR': {'buying': 1.8512, 'selling': 1.8545}, 'JPY': {'buying': 648.8100000000001, 'selling': 653.11},
#              'BGN': {'buying': 3.8194, 'selling': 3.8694}, 'RON': {'buying': 1.5443, 'selling': 1.5645},
#              'RUB': {'buying': 0.09352, 'selling': 0.09474}, 'IRR': {'buying': 1.6469999999999998, 'selling': 1.6680000000000001},
#              'CNY': {'buying': 0.97431, 'selling': 0.98706}, 'PKR': {'buying': 0.04316, 'selling': 0.04372},
#              'QAR': {'buying': 1.8993, 'selling': 1.9241}})

#   date = datetime.datetime(2020, 5, 14)
#   cur_dict = get_data(date)
#   if cur_dict == d1:
#       print("******!!!!!!*****")
#   for key in cur_dict:
#       if cur_dict[key] == d1[key]:
#         print("yey")
#       else:
        
#         print(f"cur_dict[{key}]")
#         print(cur_dict[key], "\n")

#         print(f"d1[{key}]")
#         print(d1[key], "\n")

#   date = datetime.datetime(2020, 5, 16)
#   cur_dict = get_data(date)
#   print(cur_dict)
