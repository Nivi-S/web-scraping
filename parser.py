#from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import pressSource as ps
import urllib3
#import flask


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parseHTML(str_url):

    content = requests.get(str_url, verify = False)
    soup = BeautifulSoup(content.text, 'html.parser')


    if bool(re.search('.*cdc.*', str_url)):
        searched_word = 'Total'

    if bool(re.search('.*usc.*', str_url)):
        searched_word = 'STATUS'

    if bool(re.search('.*lacounty.*', str_url)):
        searched_word = 'total'

    if bool(re.search('.*ucla.*', str_url)):
        searched_word = 'STATUS'

    results = soup.find_all(string=re.compile(
        '.*{0}.*'.format(searched_word)), recursive=True)
    print('results =', results)

    date = soup.find_all(string=re.compile('[ADFJMNOS]\w* [\d]{1,2},* [\d]{4}'))
    print("Date=", date[0])

    for content in results:
        words = content.split()
        for index, word in enumerate(words):
            # If the content contains the search word twice or more this will fire for each occurence
            if word == searched_word:
                print("Content= ", content, "\n")#('Results: "{0}"'.format(content))

    #print("\n Title =", soup.title.text)
    print("Source =", str_url, "\n ================ \n")
    #CDC = ps.pressSource(ps.level.NATIONAL, str_url)




if __name__ == "__main__":
    url = 'https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html'
    parseHTML(url)
    parseHTML('https://sites.usc.edu/coronavirus/')
    parseHTML('http://publichealth.lacounty.gov/media/Coronavirus/')
    #parseHTML('https://www.uclahealth.org/body.cfm?id=1397&action=detail&ref=3976&fr=true')
    parseHTML('https://newsroom.ucla.edu/stories/coronavirus-information-for-the-ucla-campus-community')


# ============================
