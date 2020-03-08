from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
#import requests
import re
import pressSource

driver = webdriver.Chrome()
url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html"

driver.get("https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
#cases = soup.find_all("div", class_="card-body bg-white")

searched_word= 'Total'
results = soup.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)
#print (results)


for content  in results:
    words = content.split()
    for index, word in enumerate(words):
        # If the content contains the search word twice or more this will fire for each occurence
        if word == searched_word:
            print ('Results: "{0}"'.format(content))

# next_word = 'reporting'
# next_results = soup.find_all(string=re.compile('.*{0}.*'.format(next_word)), recursive=True)


# for cont in next_results:
#     words = cont.split()
#     for index, word in enumerate(words):
#         # If the content contains the search word twice or more this will fire for each occurence
#         if word == next_word:
#             print ('States: "{0}"'.format(cont))


# for tag in cases.find_all("li"):
# 	print("{0}: {1}".format(tag.name, tag.text))

print (soup.title.text)

#============================

# for a in table.findAll('td', {'rowspan'}):
# 	timestamp=a.find('span', class_='nowrap')
# 	printf(timestamp.extract())
# 	#occurance=a.find('td', attrs={'rowspan'})
# timestamp.append(timestamp)
# occurance.append(occurance)


# df = pd.DataFrame({'Time':time,'Occurance':occurance}) 
# df.to_csv('products.csv', index=False, encoding='utf-8')