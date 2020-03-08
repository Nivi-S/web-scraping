# from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import pressSource as ps
import urllib3
from flask import jsonify
# import flask


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def extract_num_cases(sentence, word_set):
    delta = 25
    numbers = []
    for word in word_set:
        idx_char = sentence.find(word)
        if idx_char != -1:
            # Found the key word, now look for the number of cases close to the key word, using regex pattern matching
            search_range = (max(0, idx_char - delta),
                            min(len(sentence), idx_char + delta))
            # print(sentence[search_range[0]:search_range[1]])

            num = re.search(
                '(\s[0-9]+|one|two|three|four|five|six|seven|eight|nine|ten)',  sentence[search_range[0]:search_range[1]])
            if num is not None:

                matching = num.group(0)
                convert = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6',
                           'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10'}

                print("Pattern matching:", word_set)
                print(matching)
                if matching in convert:
                    matching = convert[matching]
                numbers.append(int(matching.strip()))

    # print("Sentence's set of numbers", numbers)
    return numbers


def extract_date(soup):
    date_sentences = soup.find_all(string=re.compile(
        '[ADFJMNOS]\w* [\d]{1,2},* [\d]{4}'))

    if len(date_sentences) == 0:
        date = ""
    else:
        date = re.search(
            '[ADFJMNOS]\w* [\d]{1,2},* [\d]{4}', date_sentences[0]).group()
    return date


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

    elif bool(re.search('.lapublichealth.*', str_url)):
        press_source = ps.pressSource("LA", str_url)
    else:
        print("Site not recognized. We are not monitoring this site yet. Exiting")
        exit(1)

    # Set the date value

    press_source.date = extract_date(soup)
    print("Date = ", press_source.date)
    print("Source =", str_url, "\n ================ \n")

    # Return sentences containing these general hit words
    hit_words = {'STATUS', 'status', 'Total', 'total', 'cases'}
    hit_results = []
    for word in hit_words:
        hit_results.extend(soup.find_all(string=re.compile(
            '.*{0}.*'.format(word)), recursive=True))

    hit_results = [el.replace('\xa0', ' ') for el in hit_results]

    print("Hit results:")
    for i, hit in enumerate(hit_results):
        print(i, hit)
    print("=================================")

    # Further parse sentences with hit words to extract number of positive and death cases
    positive_words = {'positive cases', 'Positive cases',
                      'confirmed cases', 'cases confirmed', 'Total cases',
                      'total cases', 'total number of cases', 'Total number of cases'}
    death_words = {'deaths', 'death'}

    # Examine words close to the hit
    positive_numbers = []
    death_numbers = []
    for idx_sent, sentence in enumerate(hit_results):
        print(idx_sent, sentence)
        np = extract_num_cases(sentence, positive_words)
        nd = extract_num_cases(sentence, death_words)

        if np is not None:
            positive_numbers.extend(np)
        if nd is not None:
            death_numbers.extend(nd)
        # print(len(ans), len(positive_numbers))
        # positive_numbers.union(extract_num_cases(sentence, positive_words))

        # This part I'm not quite sure about. I'm assuming that the FIRST encounter of a number
        # that exists close to a key phrase is the correct number of cases.
        # This is a NLP issue, it depends on how people phrase the information. But in the cases
        # we've looked at, this is sufficient.

    if len(positive_numbers) > 0:
        press_source.set_confirmed(max(positive_numbers))
    else:
        press_source.set_confirmed(0)

    if len(death_numbers) > 0:
        press_source.set_deaths(max(death_numbers))
    else:
        press_source.set_deaths(0)

    print("Confirmed: ", press_source.confirmed)
    print("Deaths: ", press_source.deaths)

    return jsonify(
        confirmed=press_source.confirmed,
        deaths=press_source.deaths,
        level=press_source.level,
        url=press_source.url,
        date=press_source.date
    )


if __name__ == "__main__":
    #url = 'https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html'
    #url = 'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/ncov2019.aspx'
    url = 'https://twitter.com/lapublichealth/status/1236398593226895360'
    # url = 'http://publichealth.lacounty.gov/media/Coronavirus/'
    # url = 'https://sites.usc.edu/coronavirus/'
    # url = 'https://newsroom.ucla.edu/stories/coronavirus-information-for-the-ucla-campus-community'
    scrapeHTML(url)

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
