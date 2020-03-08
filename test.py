from selenium import webdriver
from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")
print(soup.title.text)
