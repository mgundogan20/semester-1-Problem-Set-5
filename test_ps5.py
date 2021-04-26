from curr import Currency
import datetime
from curr_parser import get_data
from triggers import LowTrigger,HighTrigger,AndTrigger,OrTrigger,NotTrigger
import numpy as np
from curr_database import CurrencyDatabase

def test_partone():

  fail = False

  x1 = datetime.datetime(2020, 5, 14)
  r1 = get_data(x1)
  d1 = dict({'USD': {'buying': 6.9543, 'selling': 6.9668}, 'AUD': {'buying': 4.463, 'selling': 4.4921},
             'DKK': {'buying': 1.0058, 'selling': 1.0107}, 'EUR': {'buying': 7.5122, 'selling': 7.5257},
             'GBP': {'buying': 8.4708, 'selling': 8.5149}, 'CHF': {'buying': 7.1281, 'selling': 7.1739},
             'SEK': {'buying': 0.7031, 'selling': 0.71038}, 'CAD': {'buying': 4.9269, 'selling': 4.9491},
             'KWD': {'buying': 22.3556, 'selling': 22.6481}, 'NOK': {'buying': 0.6799, 'selling': 0.68447},
             'SAR': {'buying': 1.8512, 'selling': 1.8545}, 'JPY': {'buying': 648.8100000000001, 'selling': 653.11},
             'BGN': {'buying': 3.8194, 'selling': 3.8694}, 'RON': {'buying': 1.5443, 'selling': 1.5645},
             'RUB': {'buying': 0.09352, 'selling': 0.09474}, 'IRR': {'buying': 1.6469999999999998, 'selling': 1.6680000000000001},
             'CNY': {'buying': 0.97431, 'selling': 0.98706}, 'PKR': {'buying': 0.04316, 'selling': 0.04372},
             'QAR': {'buying': 1.8993, 'selling': 1.9241}})

  if r1 != d1:
    fail = True
    print("Problem.")

  x2 = datetime.datetime(2020, 5, 16)
  r2 = get_data(x2)

  if r2 != {}:
    fail = True

  assert not fail
  if fail:
    return 0
  else:
    print("Success in part 1")
    return 20


def test_parttwoa():

  fail = False

  total_days = 10
  c = Currency("EUR", total_days)
  np.random.seed(42)
  c.BUY = 5.0 * np.ones(total_days) + np.random.rand(total_days)
  c.SELL = c.BUY + 0.1

  if ((c.calc_change(0, 7, "BUY") - 9.147499433551728) > 0.1):
    fail = True
    print("Problem in calc_change")

  if ((c.calc_volatility(2, 9, "SELL") -  0.08915349751779685) > 0.1):
    fail = True
    print("Problem in calc_volatility")

  if ((c.calc_max(4, 9, "SELL") - 5.966176145774935) > 0.1):
    fail = True
    print("Problem in calc_max")

  if ((c.calc_mean(4, 9, "SELL") - 5.467477586092996) > 0.1):
    fail = True
    print("Problem in calc_mean")

  if ((c.calc_min(0, 3, "BUY") -  5.950714306409916) > 0.1) :
    fail = True
    print("Problem in calc_min")

  assert not fail
  if fail:
    return 0
  else:
    print("Success: part2a")
    return 20


def test_parttwob():

  fail = False

  # Params
  db_start_date = (1, 4, 2018)
  db_end_date = (15, 4, 2018)

  # Database Constructor
  tcmb = CurrencyDatabase(db_start_date,db_end_date)

  # Testing functions
  v1 = tcmb.conv2date(db_start_date)
  if datetime.datetime(2018, 4, 1) != v1:
    print(f"conv2date problem! Wrong val: {v1}")
    fail = True

  v2 = tcmb.date2idx(db_start_date)
  if v2 != 0:
    print(f"date2idx problem! Wrong val: {v2}")
    fail = True

  v3 = tcmb.date2idx((3, 4, 2018))
  if v3 != 2:
    print(f"date2idx problem! Wrong val: {v3}")
    fail = True

  v4 = tcmb.idx2date(0)
  if datetime.datetime(2018, 4, 1) != v4:
    print(f"idx2date problem! Wrong val: {v4}")
    fail = True

  assert not fail
  if fail:
    return 0
  else:
    print("SUCCESS: Part IIb")
    return 25

def test_partthree():

  fail = False
  total_days = 30
  c = Currency("EUR", 30)
  np.random.seed(42)
  c.BUY = 5.0 * np.ones(total_days) + np.random.rand(total_days)
  c.SELL = c.BUY + 0.1

  t1 = LowTrigger('MIN', 'SELL', 5.1, 2, 5, "",  "")
  t2 = HighTrigger('VOL', 'BUY', 0.01, 0, 7, "",  "")
  t3 = HighTrigger('MEAN', 'BUY', 5.0, 2, 5, "",  "")
  t4 = NotTrigger(t1)
  t5 = OrTrigger(t1,t2)
  t6 = AndTrigger(t4,t3)
  t7 = AndTrigger(t1,t3)
  t8 = NotTrigger(t4)
  t9 = LowTrigger('CHG', 'BUY', 1.2, 2, 5, "",  "")
  t10 = HighTrigger('MEAN', 'BUY', 5.0, 2, 5, "",  "")

  if t1.evaluate(c):
    fail = True

  if not t2.evaluate(c):
    fail = True

  if not t3.evaluate(c):
    fail = True

  if not t4.evaluate(c):
    fail = True

  if not t5.evaluate(c):
    fail = True

  if not t6.evaluate(c):
     fail = True

  if t7.evaluate(c):
    fail = True

  if t8.evaluate(c):
    fail = True

  if not t9.evaluate(c):
    fail = True

  if not t10.evaluate(c):
    fail = True

  assert not fail
  if fail:
    return 0
  else:
    print("SUCCESS: Part III")
    return 25