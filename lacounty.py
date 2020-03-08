from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
#import requests
import re
#import pressSource

driver = webdriver.Chrome()
url = "http://publichealth.lacounty.gov/media/Coronavirus/"

driver.get("http://publichealth.lacounty.gov/media/Coronavirus/")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
#cases = soup.find_all("div", class_="card-body bg-white")

searched_word= 'total'
results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
#print (results)


for content  in results:
    words = content.split()
    for index, word in enumerate(words):
        # If the content contains the search word twice or more this will fire for each occurence
        if word == searched_word:
            statement = content
            print (content)#('Results: "{0}"'.format(content))



print (soup.title.text)
