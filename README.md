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



# Getting historic prices
<a id = "link1"></a>


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
            "startDate" : dt.datetime(2022,8,1),
            "needExtendedHoursData": True
        }
instruments = ["AAPL","TSLA","GOOG","MSFT","AMZN","AMD","NVDA","BBBY","GME","SPY","/ES"]
d = client.get_price_history(symbols = instruments, params= params)
d[-1] #
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
   'volume': 603,
   'datetime': 1659546960000},
  ...],
 'symbol': 'ES',
 'empty': False}

~~~



# Getting Option chain
<a id = "link2"> </a>




# Search instruments
<a id = "link3"> </a>




# Get instruments
<a id = "link4"> </a>