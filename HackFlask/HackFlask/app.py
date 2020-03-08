from flask import Flask, render_template, request
import scraper as sc
#import requests


import urllib3
# import flask

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# from flask import Flask, render_template, request
# app = Flask(__name__)
#
#
# @app.route("/")
# def hello():
#     return render_template("index.html")
#
#
# if __name__ == "__main__":
# 	app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)


# =================

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template("index.html")


@app.route("/test/", methods=['GET', 'POST'])
def test():
    data = "testtttt"
    return data


@app.route("/UCLA/")
def getUCLAnews():
    return sc.scrapeHTML('https://newsroom.ucla.edu/stories/coronavirus-information-for-the-ucla-campus-community')


@app.route("/USC/")
def getUSCnews():
    # press_source = sc.scrapeHTML('https://sites.usc.edu/coronavirus/')
    # return str(press_source.confirmed)
    return sc.scrapeHTML('https://sites.usc.edu/coronavirus/')


@app.route("/LAC/")
def getLACnews():
    return sc.scrapeHTML('http://publichealth.lacounty.gov/media/Coronavirus/')


@app.route("/CA/")
def getCAnews():
    return sc.scrapeHTML('https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/Immunization/ncov2019.aspx')


@app.route("/CDC/")
def getCDCnews():
    return sc.scrapeHTML('https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, passthrough_errors=True)
