from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template("index.html", data="testtttt")

@app.route("/test/", methods=['GET', 'POST'])
def test():
    data = "testtttt"
    return data

# @app.route("/UCLA/")
# def getUCLAnews():
#     # ()
#
#
# @app.route("/USC/")
# def getUSCnews():
#     return parseHTML('https://sites.usc.edu/coronavirus/')
#
#
# @app.route("/LAC/")
# def getLACnews():
#
#
# @app.route("/CA/")
# def getCAnews():
#
#
# @app.route("/CDC/")
# def getCDCnews():


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, passthrough_errors=True)

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

