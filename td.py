import requests
from bs4 import BeautifulSoup
from urllib import parse
import time
import datetime as dt


class client:
    def __init__(self, id, password, c_key, redirect_url):
        self.id = id
        self.pw = password
        self.c_key = c_key
        self.redirect_url = redirect_url
        self.auth_code = None
        self.refresh_token = None # this will be valid for 90 days
        self.access_token = None # needs to be updated every 30 mins
        self.expire_time = None

    def authenticate(self):
        if self.auth_code is None:
            redirect = parse.quote(self.redirect_url, safe = "")
            url  = f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={redirect}&client_id={self.c_key}%40AMER.OAUTHAP"
            with requests.Session() as session:
                # get the hidden inputs first
                r_get = session.get(url, allow_redirects= True)
                soup = BeautifulSoup(r_get.text, "lxml")
                hidden_inputs = soup.findAll("input")
                form_params = {}

                for elements in hidden_inputs:
                    name = elements.get("name")
                    value = elements.get("value")
                    if value != "" and name != "reject":
                        form_params[name] = value

                # add in user id and pw, this is NOT the developer account's user id and pw but the trading account's id and pw
                form_params["su_username"] = self.id
                form_params["su_password"] = self.pw
                
                # this will refresh the page, that contains a new form that asks for permission 
                r_post = session.post(url, data = form_params)

                # post again to allow

                try:
                    r_post = session.post(url, data = {"authorize" : "Allow"})
                except requests.exceptions.ConnectionError as error:
                    auth_code = error.request.url

                
                
                # the actual auth code is only part of the url, all characters behind "="
                auth_code = auth_code[auth_code.index("=") + 1:]

                # decode the auth code
                auth_code = parse.unquote(auth_code)
                self.auth_code = auth_code

                session.close()

                return None
        else:
            return None
        

    def initiate_tokens(self):
        url = "https://api.tdameritrade.com/v1/oauth2/token"
        
        data = {
            "grant_type" : "authorization_code",
            "access_type" : "offline",
            "code" : self.auth_code,
            "client_id": self.c_key,
            "redirect_uri": self.redirect_url
        }
        r_post = requests.post(url, data= data).json()
        self.access_token = r_post["access_token"]
        self.refresh_token = r_post["refresh_token"]
        self.expire_time = time.time() + 25 * 60 # refresh in 25 mins
        return None


    def get_access_token(self):
        if time.time() < self.expire_time:
            return self.access_token
        else:
            url = "https://api.tdameritrade.com/v1/oauth2/token"

            data = {
                "grant_type" : "refresh_token",
                "refresh_token" : self.refresh_token,
                "client_id" : self.c_key,
                "redirect_uri" : self.redirect_url
                 }

            r_post = requests.post(url, data = data).json()
            self.access_token = r_post["access_token"]
            self.expire_time = time.time() + 25 * 60 # refresh in 25 mins
            return self.access_token


    def login(self):
        self.authenticate()
        self.initiate_tokens()
        return None

# Price History
# params 
# {
# "periodType":""
# "period":"",
# "frequencyType":"",
# "frequency":"",
# "endDate":"",
# "startDate":"",
# "needExtendedHoursData":""
# }



    def price_history_threading(self, stocks, params):
        '''
        how the param works

        periodType:
        period:
        frequencyType:
        frequency:
        endDate:
        startDate:

        '''
        symbol = None
        url = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory"
        pass
        
        # additional params
        params["apikey"] = self.c_key
        header = "Bearer " + self.get_access_token()
        data = requests.get(url, headers = {'Authorization' : header}, params = params).json()
        pass
        

        
    def price_history(self, stock, params):
        symbol = stock
        url = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory"
        
        # additional params
        params["apikey"] = self.c_key
        header = "Bearer " + self.get_access_token()
        data = requests.get(url, headers = {'Authorization' : header}, params = params).json()
        return data["candles"]
        


  




    