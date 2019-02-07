#mintos
import requests
from lxml import html


def login_to_account(session_requests, login_url, payload, token_name):

    #extract token
    result = session_requests.get(login_url)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='"+token_name+"']/@value")))[0]
    #put found token into login data dict
    payload[token_name]=authenticity_token

    #get page after login
    result = session_requests.post(
	    login_url, 
	    data = payload, 
	    headers = dict(referer=login_url)
        )

def scrape_dashboard(session_requests, url, value_path):
#scrape mintos home screen

    result = session_requests.get(
	    url, 
	    headers = dict(referer = url)
        )
    tree = html.fromstring(result.content)

    value = tree.xpath(value_path)[0] #path to portfolio value
    return(value.text)


#scrape mintos
payload_mintos= { "_username": "",
        "_password": ".",
        "_csrf_token": "J33QqFBnl5Gial_6RqLcd26fXl4GqvXx8krm1C56914"
        }
token_name_mintos ="_csrf_token"
session_requests = requests.session()
login_url_mintos = "https://www.mintos.com/en/login"

login_to_account(session_requests, login_url_mintos, payload_mintos,token_name_mintos)

url_mintos ="https://www.mintos.com/en/overview/"
value_path_mintos="//li[@class='overview-box']/div/div[@class='header']/div[@class='value']"


account_value = scrape_dashboard(session_requests, url_mintos, value_path_mintos)
print(account_value)



