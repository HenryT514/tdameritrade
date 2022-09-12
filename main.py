import pwd
import requests
from bs4 import BeautifulSoup
from urllib import parse


class client:
    def __init__(self, id, password, c_key, redirect_url):
        self.id = id
        self.pw = password
        self.c_key = c_key
        self.redirect_url = redirect_url
        self.auth_code = None


    def authorize(self):
        if self.auth_code is None:
            redirect = parse.quote(self.redirect_url, safe = "")
            url  = f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={redirect}&client_id={self.c_key}%40AMER.OAUTHAP"
            with requests.Session() as session:
                # get the hidden inputs first
                r_get = session.get(url, allow_redirects= True)
                soup = BeautifulSoup(r_get.text, "lxml")
                hidden_inputs = soup.findAll("input")
                payload = {}

                for elements in hidden_inputs:
                    name = elements.get("name")
                    value = elements.get("value")
                    if value != "" and name != "reject":
                        payload[name] = value

                # add in user id and pw, this is NOT the developer account's user id and pw but the trading account's id and pw
                payload["su_username"] = self.id
                payload["su_password"] = self.pw
                
                # this will refresh the page, that contains a new form that asks for permission 
                r_post = session.post(url, data = payload)

                # post again allow

                try:
                    r_post = session.post(url, data = {"authorize" : "Allow"})
                except requests.exceptions.ConnectionError as error:
                    auth_code = error.request.url
                
                # the actual auth code is only part of the url, all characters behind "="
                auth_code = auth_code[auth_code.index("=") + 1:]

                # decode the auth code
                auth_code = parse.unquote(auth_code, safe = "")
                self.auth_code = auth_code

                return None
        else:
            return None
        

    def get_token(self):
        pass




    