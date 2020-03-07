from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()

timestamp=[] #List to store name of the product
occurance=[] #List to store price of the product
#ratings=[] #List to store rating of the product
driver.get("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

table = soup.find('table',class_='wikitable collapsible mw-collapsible mw-made-collapsible')
for a in table.findAll('td', {'rowspan'}):
	timestamp=a.find('span', class_='nowrap')
	printf(timestamp.extract())
	#occurance=a.find('td', attrs={'rowspan'})
timestamp.append(timestamp)
occurance.append(occurance)


df = pd.DataFrame({'Time':time,'Occurance':occurance}) 
df.to_csv('products.csv', index=False, encoding='utf-8')