from __future__ import print_function
from selenium import webdriver
import re
from selenium.webdriver.firefox.options import Options
from urllib2 import Request , urlopen
import time
from datetime import datetime
import sys
import time

from bs4 import BeautifulSoup

#sudo mv geckodriver /usr/local/bin/
#https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu

if len(sys.argv) ==2:
    filteredlink = sys.argv[1]
    print('...' + sys.argv[1][75:])
    print('Using custom link')
else:
    filteredlink = "https://www.mintos.com/en/available-loans/secondary-market/?currencies[]=978&lender_groups[]=19&lender_groups[]=8&lender_groups[]=9&lender_groups[]=14&lender_groups[]=7&lender_groups[]=27&lender_groups[]=33&lender_groups[]=22&lender_groups[]=3&lender_groups[]=29&lender_groups[]=4&lender_groups[]=11&lender_groups[]=6&lender_groups[]=35&lender_groups[]=32&lender_groups[]=20&lender_groups[]=30&lender_groups[]=17&lender_groups[]=26&lender_groups[]=1&lender_groups[]=23&lender_groups[]=16&lender_groups[]=25&lender_groups[]=13&lender_groups[]=28&lender_groups[]=21&lender_groups[]=24&lender_groups[]=36&lender_groups[]=34&lender_groups[]=31&with_buyback=1&statuses[]=2048&max_premium=-0.3&sort_field=ytm&sort_order=ASC&max_results=20&page=1"
    print('Using default filters')

options = Options()
options.add_argument("--headless")
print('Running in headless mode')

browser = webdriver.Firefox(options = options)
browser.get(filteredlink)
time.sleep(10)
#process page
text = browser.page_source.encode('utf-8').strip()
print("Page loaded")
browser.close()
 
#find IDs 
pattern = re.compile('/en/\d{6,8}-\d{2}')
results = re.findall(pattern, text)
print(str(len(results)) + " " + "loan IDs found")

#get all the dates
loandict ={}
for code in results:
    #load page
    page = 'https://www.mintos.com/en/' + code[4:]
    req = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    #parse
    soup = BeautifulSoup(webpage, 'html.parser')
    name_box = soup.find("tr", class_="m-loan-entry m-loan-entry--no-padding ")
    box_one = name_box.find("td", class_="m-labeled-col")
    m = re.search('..\...\.201.', box_one.text)
    x = m.group()
    #add to dict
    loandict[code[4:]]= x

#get todays date
current_time = time.strftime("%d.%m.%Y")

#calculate days left
for id in loandict:
    current = datetime.strptime(current_time, '%d.%m.%Y')
    lastpay = (datetime.strptime(loandict[id], '%d.%m.%Y'))
    dayspassed = current - lastpay
    daysleft = 60 - dayspassed.days
    loandict[id] = daysleft

outputnum = 10 
print("top "+ str(outputnum) + " results:")
for loan in sorted(loandict, key=loandict.get)[:outputnum]:
    print(loan + ": " + str(loandict[loan]) + " days left " + "https://www.mintos.com/en/" +loan)

