# from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import pressSource as ps
import urllib3
# import flask


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrapeHTML(str_url):
    # Check that the URL is valid
    content = requests.get(str_url, verify=False)
    if content.status_code != 200:
        print("Error in HTTP Request. Exiting with status code ",
              content.status_code)
        exit(1)

    soup = BeautifulSoup(content.text, 'html.parser')

    # Create a press source object based on the string url
    if bool(re.search('.*cdc.*', str_url)):
        press_source = ps.pressSource("CDC", str_url)

    elif bool(re.search('.*usc.*', str_url)):
        press_source = ps.pressSource("USC", str_url)

    elif bool(re.search('.*lacounty.*', str_url)):
        press_source = ps.pressSource("LA", str_url)

    elif bool(re.search('.*ucla.*', str_url)):
        press_source = ps.pressSource("UCLA", str_url)

    elif bool(re.search('.*cdph.*', str_url)):
        press_source = ps.pressSource("CA", str_url)
    else:
        print("Site not recognized. We are not monitoring this site yet. Exiting")
        exit(1)

    # Set the date value
    date_sentences = soup.find_all(string=re.compile(
        '[ADFJMNOS]\w* [\d]{1,2},* [\d]{4}'))

    if len(date_sentences) == 0:
        date = ""
    else:
        date = re.search(
            '[ADFJMNOS]\w* [\d]{1,2},* [\d]{4}', date_sentences[0]).group()

    press_source.date = date
    print("Date = ", date)
    print(press_source.date)
    print("Source =", str_url, "\n ================ \n")

    # Return sentences containing these hit words
    hit_words = {'STATUS', 'status', 'Total', 'total', 'cases'}
    hit_results = []
    for word in hit_words:
        hit_results.extend(soup.find_all(string=re.compile(
            '.*{0}.*'.format(word)), recursive=True))

    hit_results = [el.replace('\xa0', ' ') for el in hit_results]

    # print('hit_results =', hit_results)
    print("Hit results:")
    for i, hit in enumerate(hit_results):
        print(i, hit)

    # Further parse sentences with hit words to extract number of positive and death cases
    positive_words = {'positive cases', 'Positive cases',
                      'confirmed cases', 'cases confirmed', 'Total cases',
                      'total cases', 'total number of cases', 'Total number of cases'}
    death_words = {'deaths', 'death'}

    # Examine words one or two away from the hit
    positive_phrase_locations = []
    negative_phrase_locations = []
    delta = 40
    for idx_sent, sentence in enumerate(hit_results):
        for word in positive_words:
            idx_char = sentence.find(word)
            if idx_char != -1:
                search_range = (max(0, idx_char - delta),
                                min(len(sentence)-1, idx_char + delta))
                print(idx_sent, sentence[search_range[0]:search_range[1]])
                print(
                    re.match('.*\s[1-9]*.*', sentence[search_range[0]:search_range[1]]).group(0))

                positive_phrase_locations.append((idx_sent, idx_char))
        for word in death_words:
            idx_char = sentence.find(word)
            if idx_char != -1:
                negative_phrase_locations.append((idx_sent, idx_char))

    #print(positive_phrase_locations, negative_phrase_locations)


if __name__ == "__main__":
    url = 'https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html'
    scrapeHTML(url)
    # scrapeHTML('https://sites.usc.edu/coronavirus/')
    # scrapeHTML('http://publichealth.lacounty.gov/media/Coronavirus/')
    # scrapeHTML(
    #    'https://newsroom.ucla.edu/stories/coronavirus-information-for-the-ucla-campus-community')
    # scrapeHTML(
    #    'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/ncov2019.aspx')

# ============================

    # print("*****************************", date)
    # print("Date =", date[0])

    # for res in hit_results:
    #     words = res.split()
    #     for index, word in enumerate(words):
    #         # If the content contains the search word twice or more this will fire for each occurence
    #         if word == searched_word:
    #             # ('Results: "{0}"'.format(content))
    #             print("Content= ", content, "\n")

    # print("\n Title =", soup.title.text)
