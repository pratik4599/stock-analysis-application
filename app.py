import pandas as pd
import time
import json
from flask import Flask, Response, flash, request, render_template, stream_with_context, send_file
from requests.api import get
from datetime import datetime
from flask_pymongo import PyMongo
import urllib
import os


app = Flask(__name__)


#########################################################################################################
# to clear list before starting server
visited_obj = []
with open('visited.json', 'w') as fp:
    json.dump(visited_obj, fp)


#########################################################################################################


@app.route("/prev_day", methods=["GET", "POST"])
def prev_day():
    if request.method == "POST":
        prev_date = request.form.get("prev_date")
        
        prev_date = int(prev_date)
        # print(prev_date)

        prev_month = request.form.get("prev_month")
        prev_month = int(prev_month)
        # print(prev_month)

        prev_year = request.form.get("prev_year")
        prev_year = int(prev_year)
        # print(prev_year)

        label_yr_month = request.form.get("label_yr_month")
        label_yr_month = str(label_yr_month)
        # print(label_yr_month)

        level = request.form.get("level")
        level = str(level)
        # print(level)

        access_token = request.form.get("access_token")
        access_token = str(access_token)
        # print(access_token)

        di = dict()
        di['accesstoken'] = access_token
        with open('data.json', 'w') as fp:
            json.dump(di, fp)

        def fun0():
            with open('predata.json', 'r') as fp:
                predata_obj = json.load(fp)
            predata_obj["prev_date"] = prev_date
            predata_obj["prev_month"] = prev_month
            predata_obj["prev_year"] = prev_year
            predata_obj["label_yr_month"] = label_yr_month
            predata_obj["level"] = level

            with open('predata.json', 'w') as fp:
                json.dump(predata_obj, fp)
        fun0()

        return "done"


@app.route("/access_token", methods=["GET", "POST"])
def access_token():
    if request.method == "POST":
        def fun1():
            from kite_autologin import autologin
            autologin()
        print('calling autologin function')
        fun1()
        return "done"


@app.route("/pre_bullish", methods=["GET", "POST"])
def pre_bullish():
    if request.method == "POST":
        def fun2():
            from pre_bullish import fun_bullish
            fun_bullish()
        print('calling pre_bullish')
        fun2()
        
        def fun3():
            from pre_bullish import prepare_nifty
            prepare_nifty()
        fun3()
        return "done"



########################################################################################################


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def render_index():
    return render_template("home.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        from post_bullish import get_bearish_dic
        dd = get_bearish_dic()
        dd = json.dumps(dd)
        return dd

    return render_template("dashboard.html")


#####################################################################################################




@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/tutorials", methods=["GET", "POST"])
def tutorials():
    return render_template("tutorials.html")

@app.route("/show_images", methods=["GET", "POST"])
def show_images():
    return render_template("show_images.html")


@app.route("/gainers_losers", methods=["GET", "POST"])
def gainers_losers():
    if request.method == "POST":
        from post_bullish import gainers_losers
        dd = gainers_losers()
        dd = json.dumps(dd)
        return dd


@app.route("/gap_up_down", methods=["GET", "POST"])
def gap_up_down():
    if request.method == "POST":
        from post_bullish import gap_up_down
        dd = gap_up_down()
        dd = json.dumps(dd)
        return dd


@app.route("/open_high_low", methods=["GET", "POST"])
def open_high_low():
    if request.method == "POST":
        from post_bullish import open_high_low
        dd = open_high_low()
        dd = json.dumps(dd)
        return dd


@app.route("/vwap_reversal", methods=["GET", "POST"])
def vwap_reversal():
    if request.method == "POST":
        from post_bullish import vwap_reversal
        dd = vwap_reversal()
        dd = json.dumps(dd)
        return dd
    

#########################################################################################################
if __name__ == "__main__":
    app.debug= True
    app.run(threaded=True, port=8000)
#########################################################################################################
