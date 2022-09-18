# TD Ameritrade API for collecting data

### Getting the items required
- Sign up for a Td ameritrade real/paper <i>Trading Account</i> 

- Sign up for a Tdameritrade <i>Developer Account</i> 
    * Sign up for a account on https://developer.tdameritrade.com/apis
    * nagivate to "myapps"  -> create new app
    * fill up the application form , name (can be anything) , callbackURL/redirectURL as (http://localhost), purpose(can be anything), order limit (can be anything)
    * wait for approval, should be approved in minutes


items needed
1. TD ameritrade trading account username
2. TD ameritrade trading account password
3. consumer/api key 
4. redirect URL



# Getting started 
API endpoints
* [get historical prices](#link1)
* [get option chain](#link2)
* [search instruments](#link3)
* [get instruments](#link4)



```python
from td import Client

client = Client(username, password, c_key, redirect_url) # trading acocunt's username and password (NOT developer's account's)
client.login()
```



# Getting historic prices <a id = "link1"></a>



~~~python
params =  {
            "periodType":"day",
            "period":10,
            "frequencyType":"minute",
            "frequency":1,
            "endDate":None,
            "startDate" :None,
            "needExtendedHoursData": True

instruments = ["AAPL"]
d = client.get_price_history(symbols = instruments, params= params)
d[0]
~~~

## Output

~~~python
{'candles': [{'open': 157.96,
    'high': 158.03,
    'low': 157.96,
    'close': 158.03,
    'volume': 1071,
    'datetime': 1662116400000},
   {'open': 158.02,
    'high': 158.02,
    'low': 158.0,
    'close': 158.0,
    'volume': 2077,
    'datetime': 1662116460000},
   {'open': 157.94,
...
    'volume': 128963,
    'datetime': 1662474840000},
   ...],
  'symbol': 'AAPL',
  'empty': False}
~~~

## Getting price history of multiple stocks
~~~python
params =  {
            "frequencyType":"minute",
            "endDate":dt.datetime(2022,9,15),
            "startDate" : dt.datetime(2022,8,1,22,30,0),
            "needExtendedHoursData": False
        }
instruments = ["AAPL","TSLA","GOOG","MSFT","AMZN","AMD","NVDA","BBBY","GME","SPY","/ES"]
d = client.get_price_history(symbols = instruments, params= params)
d[-1] # #
~~~

## Output

~~~python
{'candles': [{'open': 88.6,
   'high': 88.64,
   'low': 88.26,
   'close': 88.57,
   'volume': 47889,
   'datetime': 1659360600000},
  {'open': 88.63,
   'high': 88.94,
   'low': 88.52,
   'close': 88.94,
   'volume': 3519,
   'datetime': 1659360660000},
  {'open': 88.81,
   'high': 89.23,
   'low': 88.78,
   'close': 89.14,
   'volume': 13730,
   'datetime': 1659360720000},
  {'open': 89.11,
   'high': 89.265,
   'low': 89.11,
   'close': 89.265,
   'volume': 1589,
   'datetime': 1659360780000},
  {'open': 89.2,
...
   'volume': 300,
   'datetime': 1659547200000},
  ...],
 'symbol': 'ES',
 'empty': False}

~~~


## Converting output into dataframe

~~~python
df = pd.DataFrame()
for data in d:
    temp = pd.DataFrame(data["candles"])
    temp["symbol"] = data["symbol"]
    temp["datetime"] = pd.to_datetime(temp.datetime, unit = "ms").dt.tz_localize("UTC").dt.tz_convert("Singapore")
    df = pd.concat([df,temp])

df
~~~

## Output

~~~ 
open	high	low	close	volume	datetime	symbol
0	161.010	161.91	161.010	161.6700	1354707	2022-08-01 21:30:00+08:00	AAPL
1	161.655	161.74	161.290	161.3219	235573	2022-08-01 21:31:00+08:00	AAPL
2	161.335	161.39	161.160	161.2000	227469	2022-08-01 21:32:00+08:00	AAPL
3	161.190	161.78	161.140	161.6600	314502	2022-08-01 21:33:00+08:00	AAPL
4	161.650	161.81	161.570	161.6500	258539	2022-08-01 21:34:00+08:00	AAPL
...	...	...	...	...	...	...	...
11912	90.740	90.75	90.491	90.5100	17501	2022-09-15 03:55:00+08:00	ES
11913	90.510	90.57	90.490	90.5700	10001	2022-09-15 03:56:00+08:00	ES
11914	90.570	90.62	90.560	90.5850	9862	2022-09-15 03:57:00+08:00	ES
11915	90.580	90.67	90.560	90.6550	22332	2022-09-15 03:58:00+08:00	ES
11916	90.655	90.74	90.650	90.7000	31125	2022-09-15 03:59:00+08:00	ES
136686 rows × 7 columns

~~~


# Getting Option chain  <a id = "link2"> </a>

~~~ python
params= {
            'contractType' : "ALL" ,
            'strikeCount' : None,
            'includedQuotes' : "TRUE" ,
            'strategy' : None,
            'interval' : None,
            'strike' : None,
            'range' : None,
            'fromDate' : None,
            'toDate' : None,
            'volatility' : None,
            'underlyingPrice' : None,
            'interestRate' : None,
            'daysToExpiration' : None,
            'expMonth' : None,
            'optionType' : "ALL"
        }
instruments = ["AAPL","TSLA","TSLA","MSFT","AMZN","AMD","NVDA","BBBY","GME","SPY","/ES"]
d = client.get_option_chain(symbols = instruments, params= params)
d
~~~

## Output

~~~

[{'symbol': 'AAPL',
  'status': 'SUCCESS',
  'underlying': None,
  'strategy': 'SINGLE',
  'interval': 0.0,
  'isDelayed': True,
  'isIndex': False,
  'interestRate': 0.1,
  'underlyingPrice': 151.31,
  'volatility': 29.0,
  'daysToExpiration': 0.0,
  'numberOfContracts': 1800,
  'putExpDateMap': {'2022-09-23:6': {'70.0': [{'putCall': 'PUT',
      'symbol': 'AAPL_092322P70',
      'description': 'AAPL Sep 23 2022 70 Put (Weekly)',
      'exchangeName': 'OPR',
      'bid': 0.0,
      'ask': 0.01,
      'last': 0.0,
      'mark': 0.01,
      'bidSize': 0,
      'askSize': 205,
      'bidAskSize': '0X205',
      'lastSize': 0,
      'highPrice': 0.0,
...
  'volatility': 0.0,
  'daysToExpiration': 0.0,
  'numberOfContracts': 6,
  'putExpDateMap': {},
  'callExpDateMap': {}}]


~~~




# Search instruments <a id = "link3"> </a>

~~~ python

d = client.search_instruments(symbol = "AAPl",params = {"projection" : "fundamental"})
d
~~~

### Output

~~~ python
{'AAPL': {'fundamental': {'symbol': 'AAPL',
   'high52': 182.94,
   'low52': 129.04,
   'dividendAmount': 0.92,
   'dividendYield': 0.61,
   'dividendDate': '2022-08-05 00:00:00.000',
   'peRatio': 24.90102,
   'pegRatio': 1.344299,
   'pbRatio': 41.74322,
   'prRatio': 6.24929,
   'pcfRatio': 21.84594,
   'grossMarginTTM': 43.31427,
   'grossMarginMRQ': 43.25631,
   'netProfitMarginTTM': 25.70896,
   'netProfitMarginMRQ': 23.43567,
   'operatingMarginTTM': 30.53321,
   'operatingMarginMRQ': 27.81615,
   'returnOnEquity': 162.8163,
   'returnOnAssets': 29.91313,
   'returnOnInvestment': 46.50076,
   'quickRatio': 0.8228,
   'currentRatio': 0.86463,
   'interestCoverage': 0.0,
   'totalDebtToCapital': 67.31853,
   'ltDebtToEquity': 162.9752,
...
  'cusip': '037833100',
  'symbol': 'AAPL',
  'description': 'Apple Inc. - Common Stock',
  'exchange': 'NASDAQ',
  'assetType': 'EQUITY'}}

~~~


# Get instruments <a id = "link4"> </a>
