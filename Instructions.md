# TCMB Currency Database

# Deadline: 17/01/2021 - 11:00pm

Required reading: Section 4.5 & 4.6 from your textbook.

## Part 0: Overview

In this assignment, you will implement a small currency database for the Central Bank of Turkey (TCMB), which holds TRY (Turkish Lira) foreign exchange rates for a short interval. In this database, you will implement alarm mechanisms to alert the currency analysts if a specific threshold is violated, for example, when EUR/TRY is lower than 5.2.

You will complete your implementation in three parts. In the first part, you will code a parser, text-processor for a webpage in XML format. This parser is going to fetch the data stored in the [Central Bank of Turkey webpage](https://www.tcmb.gov.tr/kurlar/201806/29062018.xml).

This link returns daily currency rates based on URL. The first segment of the link is the year-month format (2018 and 06). The second segment of the link is in the day-month-year format. You will extract foreign exchange (forex) buying and selling data from this tabular data with the code inside "curr_parser.py".

In the second part, you will implement a currency class (in currency.py) that holds this parsed exchange data. Each currency will be an instance of this class, and you will keep this data in an indexed format. Then, you will aggregate these instances inside a master-class, called `CurrencyDatabase`. This class will implement the high-level operations such as indexing, running triggers, writing reports, etc.

In the final part, you will implement the alarm mechanism for this database, namely, triggers. You will process trigger definitions from the "triggers.txt" file provided. In each line of this file, there is a trigger configuration. You will iterate over the database and trigger an alarm if a specific threshold is violated.

We provide you a skeleton code to complete all of these parts in multiple files.

## Part I: (Text Processing) Building the Parser


1. In the "curr_parser.py" file, we have a `get_data` function, which expects a `datetime` object, parses an XML file, and returns a dictionary of currency values. The following definitions and sources may be useful for you in this part:

* To work with dates as objects, you will need a module called `datetime`. This class date contains the year, month, day, hour, minute, second, and microsecond, and implements powerful functions. For more information, please check the [Python documentation for the `datetime` module](https://docs.python.org/3/library/datetime.html).

* Extensible Markup Language (XML) is a markup language that defines a set of rules for encoding documents in a human-readable and machine-readable format. TCMB stores money data on the web in this format.

First, construct the URL as a string. For example, for June 29th of 2019, the url should be as follows:

> https://www.tcmb.gov.tr/kurlar/201806/29062018.xml

For the date-related part, you need to use the class properties of the `datetime` such as `month`. 

**Hint**: Check the `strftime` method, which returns a custom string representing the date.

2. The page is in a both human-readable and machine-readable format. We can see the source of the page by typing into a browser 

> view-source:https://www.tcmb.gov.tr/kurlar/201806/29062018.xml

or 

by going to the website 

> https://www.tcmb.gov.tr/kurlar/201806/29062018.xml

and doing right-click and then choosing the "view source". 

This way, we can see the data stored on this webpage. This page structure is called an *element-tree*. A tree is a data structure with a root value and subtrees of children with a parent node. The root-node of this XML is:

```
<Tarih_Date Tarih="29.06.2018" Date="06/29/2018"  Bulten_No="2018/125">
...

</Tarih_Date>

```

and one of the children subtrees is a currency tree, which holds daily exchange rate information: 

```
<Currency CrossOrder="0" Kod="USD" CurrencyCode="USD">
			<Unit>1</Unit>
			<Isim>ABD DOLARI</Isim>
			<CurrencyName>US DOLLAR</CurrencyName>
			<ForexBuying>4.5607</ForexBuying>
			<ForexSelling>4.5690</ForexSelling>
			<BanknoteBuying>4.5575</BanknoteBuying>
			<BanknoteSelling>4.5758</BanknoteSelling>
			<CrossRateUSD/>
			<CrossRateOther/>
		
</Currency>
```

All subtrees -except one which you should not worry about- are in the same format. All we need to do is to iterate over each subtree and extract information for currency exchange. From each subtree, we need to extract the attribute `CurrencyCode` and the information stored in the leaves including `Unit`, `ForexBuying`, and `ForexSelling`. `ForexBuying` and `ForexSelling` define the conversion rates used for money trading as explained next with an example. 

For example, for the `CurrencyCode` USD, if the `ForexSelling` is equal to 4.5690, this means by selling 1 USD, the bank will receive 4.5690 TRY in return. Similarly, if the `ForexBuying` is equal to 4.5607, this means in order to buy 1 USD, the bank needs to spend 4.5607 TRY. `Unit` is used to scale down values into readable ranges for some currencies. The value is typically 1, then we do not need to do anything but if it is greater than 1, for example 100 for some currencies, then we need to multiply both `ForexSelling` and `ForexBuying` by the `Unit`.

Please follow the instructions to extract this information as follows:

To extract the value of an attribute like `CrossOrder` or `CurrencyCode`, you can use `get` function of the tree object. For example, `currency.get('CrossOrder')` returns "0". We do not need to know its implementation in order to use this function. This is called *abstraction*.

To extract the information stored inside the leaves, you can call the `find` function of the tree object. This returns an XML-Unit object instance, which has a class property called `text` that is a string. Here, you are accessing a property of a class instance. For example, `currency.find('CurrencyName').text` returns a string "US DOLLAR". You need to cast it appropriately if you are processing numeric data.

To complete this section, please fill in the TODO part 2 in "curr_parser.py".

3. (Exception handling) As you might imagine, not all pages are available all the time, for example when the exchange market is closed. Use exception handling to catch these cases, and show a meaningful message, e.g. with the URL or date in consideration as shown in the example below.

You can test your implementation by running "curr_parser.py". We provide a small script as a tester. If you get the same output with the following, you are good to go!

```

{'USD': {'buying': 7.4689, 'selling': 7.4823}, 'AUD': {'buying': 5.4207, 'selling': 5.4561}, 'DKK': {'buying': 1.1887, 'selling': 1.1946}, 'EUR': {'buying': 8.858, 'selling': 8.8739}, 'GBP': {'buying': 9.5837, 'selling': 9.6336}, 'CHF': {'buying': 8.2078, 'selling': 8.2605}, 'SEK': {'buying': 0.84827, 'selling': 0.85705}, 'CAD': {'buying': 5.6628, 'selling': 5.6883}, 'KWD': {'buying': 24.29, 'selling': 24.6079}, 'NOK': {'buying': 0.82709, 'selling': 0.83265}, 'SAR': {'buying': 1.9912, 'selling': 1.9948}, 'JPY': {'buying': 702.9200000000001, 'selling': 707.58}, 'BGN': {'buying': 4.5035, 'selling': 4.5624}, 'RON': {'buying': 1.8134, 'selling': 1.8372}, 'RUB': {'buying': 0.09894, 'selling': 0.10023}, 'IRR': {'buying': 1.7680000000000002, 'selling': 1.791}, 'CNY': {'buying': 1.0882, 'selling': 1.1024}, 'PKR': {'buying': 0.0447, 'selling': 0.04528}, 'QAR': {'buying': 2.0392, 'selling': 2.0659}}

 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/202001/01012020.xml

```

## Part IIa: (OOP) Currency Class

We will start by implementing a `Currency` class for our database. This class will hold our currency exchange data and also provide some analysis functions such as calculating the mean, the minimum, the maximum, the change rate, and the volatility over a given interval. We will use `NumPy`, which is a fundamental package for scientific computing in Python.

You can construct a `Currency` object with two parameters only: `code` and `total_days`. `code` stands for `CurrencyCode` in your parsed XML file, a short notation for currencies (e.g., EUR, USD, JPY). `total_days` stands for the number of days that our currency data is fetched. For example, `Currency("EUR", 10)` creates a currency object for Euro for 10 days data. Initially, your data is set to 0; that's what `np.zeros(total_days)` does.


You will implement five numeric calculation functions: `mean`, `min`, `max`, `volatility`, and `change`. Each of them expects two indices; start date index, end date index, and a property to measure (`BUY` or `SELL`). For your convenience, we provide `get_data_fragment` function to extract currency data over an interval for you.

* Mean is computed by averaging all of the values inside a data fragment (`np.mean()`)

* Min is computed by finding minimum of the values inside a data fragment (`np.min()`)

* Max is computed by finding maximum of the values inside a data fragment (`np.max()`)

* Change is computed by finding the percentile difference between two dates: 

> 100.*(d2 - d1)/d1

where d2 is the value at the second date and d1 is the value at the first date. 

* Volatility is computed by finding the variance of data. (`np.var()`)


You can test your implementation by running "curr.py". We provide a small script as a tester. If you get the same output with the following, you are good to go!

```

Change:  9.147499433551728
Vol:  0.08915349751779685
Max:  5.966176145774935
Mean:  5.467477586092996
Min:  5.950714306409916

```

## Part IIb: (OOP) CurrencyDatabase Class

In this part, you will complete the master class, `CurrencyDatabase`. This class consists of `Currency` class instances for each of the currencies and date-time indexing functionality for efficiency. In "curr_database.py", we provide an initial incomplete codebase for you, your task is to complete it by implementing the date indexing mechanism as explained next. 

`CurrencyDatabase` class requires only two parameters: start date (tuple) and end date (tuple). It automatically downloads the currency information from the TCMB website, builds a simple database, and prompts a summary. Your task is to complete four functions `date_cnt`, `conv2date`, `idx2date`, `date2idx` and `__init__` function of the `CurrencyDatabase` class:

* `init()`:  Complete the data saving part. If the market is open, save each currency's data, otherwise copy the currency values from the previous day.

* `conv2date(date_tuple)`: Given a date tuple, return a datetime object.

* `date_cnt()`: Return the total number of dates between the start date and the end date. (**Hint**: Think about the case where the start and end date is the same. The resulting `date_cnt` should be 1 in this case.)

Note that this function can act as a class property thanks to the `@property` line above the function definition. This is called a *decorator* and it enables the function to act like a class property.

* `idx2date(idx)`: Given an index, this should return the `datetime` object. 

* `date2idx(target_date)`: Given a `datetime` object, returns a corresponding index for the target date. Assertions are applied to notify that the date index is outside of the dataset interval.

You can test your implementation by running "curr_database.py". We provide a small script as a tester. If you get the same output as the following, you are good to go!

```
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/01042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/07042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/08042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/14042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/15042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/21042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/22042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/23042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/28042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201804/29042018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201805/01052018.xml
 HTTP Error 404: Not Found - https://www.tcmb.gov.tr/kurlar/201805/05052018.xml
Database init completed.
Database interval: 2018-04-01 00:00:00 - 2018-05-05 00:00:00
Fetched 35 days. Market is open 23.0 days.
There are 18 currencies.
---
```
Why did we use a date indexing mechanism?

**Inline question**: If we iterate all over the dates to process data, what would be the algorithmic complexity? What is the algorithmic complexity with the help of indexing?

**Your answer**: 


## Part III: (Inheritance) Triggers

As we discussed before, the final output of our database program is triggering alarms if needed. There are five types of triggers (High, Low, Not, And, Or) which inherit trigger parent class. These triggers are raised when certain threshold conditions are satisfied. These conditions are defined in the "triggers.txt" file; a trigger configuration is given in each line. 

For example, the line 

> HIGH MEAN SELL 4.2 22/04/2018 12/05/2018

means constructing a high trigger that gives an alarm when the mean value of sell data of a currency is higher than 4.2 in between the dates 22/04/2018 - 12/05/2018. This trigger will return True if this condition is satisfied; otherwise, it will return False.

Please check `set_triggers` and `run_triggers` functions in "curr_database.py" file. In this part, your task is to complete the `Triggers` class and subclasses given inside the "triggers.py" file. Remember, for each trigger, you are inheriting the parent class and they inherit all the properties of the parent class. You will only create different evaluation functions for each type of trigger.

You can test your implementation by running the file "triggers.py". We provide a small script as a tester. If you get the same output with the following, you are good to go!

```
t1 -  False
t2 -  True
t3 -  True
t4 -  True
t5 -  True
t6 -  True
```

## Part IV: Final

You can check your code by running "main.py" file. The desired output is given in "output.txt" for you to compare.