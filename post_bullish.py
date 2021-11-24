import json
from kiteconnect import KiteConnect
from pynse import *
import pandas as pd
import requests
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)
import configparser


def quote_dic():

    # api key
    config = configparser.ConfigParser()
    config.read('credential.ini')
    api_key = config['kite']['api_key']

    # access token
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    access_token = data["accesstoken"]

    # kite object
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token=access_token)


    # pp.pprint(kite.quote("NSE:BIOCON"))
    # equity list
    with open('eq.json', 'r') as fp:
        eq_url_dic = json.load(fp)
    equity_list = list(eq_url_dic.keys())
    equity_list_quote_format_list = ['NSE:{}'.format(i) for i in equity_list]

    # api call for quote
    qd = kite.quote(equity_list_quote_format_list)
    return qd


quote_dic()
# pp.pprint(quote_dic())

def gainers_losers():

    # get quote
    dd = quote_dic()
    
    # stock:url dictionary
    with open('eq.json', 'r') as fp:
        eq_url_dic = json.load(fp)

    # gainers and losers
    name_perc_dic = {}
    li = list(dd.keys())
    for i in li:
        l = (dd[i]['last_price'])
        p = (dd[i]['ohlc']['close'])
        i = i.replace("NSE:", "")
        name_perc_dic[i] = round((float(((l-p)/p)*100)), 2)

    abc = (sorted(name_perc_dic.items(), key=lambda item: item[1]))

    top_losers = list(abc)[0:10]
    top_gainers = list(abc)[-10:]

    name_url_perc_dic_losers = {}
    for i in top_losers:
        key = i[0]
        value_perc = i[1]
        value_url = eq_url_dic[key]
        name_url_perc_dic_losers[key] = [value_perc, value_url]

    name_url_perc_dic_gainers = {}
    for i in top_gainers:
        key = i[0]
        value_perc = i[1]
        value_url = eq_url_dic[key]
        name_url_perc_dic_gainers[key] = [value_perc, value_url]

    lis_gainers_losers = [name_url_perc_dic_gainers, name_url_perc_dic_losers]
    return lis_gainers_losers





def gap_up_down():

    # get quote
    dd = quote_dic()

    # stock:url dictionary
    with open('eq.json', 'r') as fp:
        eq_url_dic = json.load(fp)

    name_gap = {}
    li = list(dd.keys())
    for i in li:
        o = (dd[i]['ohlc']['open'])
        c = (dd[i]['ohlc']['close'])
        i = i.replace("NSE:", "")
        name_gap[i] = round((float(((o-c)/c)*100)), 2)
    abc = (sorted(name_gap.items(), key=lambda item: item[1]))
    gap_down = list(abc)[0:10]
    gap_up = list(abc)[-10:]

    name_url_perc_dic_gap_down = {}
    for i in gap_down:
        key = i[0]
        value_perc = i[1]
        value_url = eq_url_dic[key]
        name_url_perc_dic_gap_down[key] = [value_perc, value_url]
    # pp.pprint(name_url_perc_dic_losers)

    name_url_perc_dic_gap_up = {}
    for i in gap_up:
        key = i[0]
        value_perc = i[1]
        value_url = eq_url_dic[key]
        name_url_perc_dic_gap_up[key] = [value_perc, value_url]
    # pp.pprint(name_url_perc_dic_gainers)

    lis_gap_up_down = [name_url_perc_dic_gap_up, name_url_perc_dic_gap_down]
    return lis_gap_up_down


def open_high_low():
    # get quote
    dd = quote_dic()

    # stock:url dictionary
    with open('eq.json', 'r') as fp:
        eq_url_dic = json.load(fp)
        
    # open == high
    name_open_equal_high = {}
    li = list(dd.keys())
    for i in li:
        o = (dd[i]['ohlc']['open'])
        h = (dd[i]['ohlc']['high'])
        i = i.replace("NSE:", "")
        if o == h:
            name_open_equal_high[i] = [round((float(((o-h)/h)*100)), 2)]

    # open == low
    name_open_equal_low = {}
    li = list(dd.keys())
    for i in li:
        o = (dd[i]['ohlc']['open'])
        l = (dd[i]['ohlc']['low'])
        i = i.replace("NSE:", "")
        if o == l:
            name_open_equal_low[i] = [round((float(((o-l)/l)*100)), 2)]

    name_url_dic_open_equal_high = {}
    for i in name_open_equal_high.keys():
        name_url_dic_open_equal_high[i] =  eq_url_dic[i]
    
    # print(name_url_dic_open_equal_high)

    name_url_dic_open_equal_low = {}
    for i in name_open_equal_low.keys():
        name_url_dic_open_equal_low[i] =  eq_url_dic[i]

    print(name_url_dic_open_equal_low)

    lis_open_high_low = [name_url_dic_open_equal_high,
                         name_url_dic_open_equal_low]
    
    return lis_open_high_low

# open_high_low()



def vwap_reversal():
    # get quote
    dd = quote_dic()

    # stock:url dictionary
    with open('eq.json', 'r') as fp:
        eq_url_dic = json.load(fp)
        
    vwap_reversal = {}
    li = list(dd.keys())
    for i in li:
        l = (dd[i]['last_price'])
        avg = (dd[i]['average_price'])
        i = i.replace("NSE:", "")
        try:
            vwap_reversal[i] = round((float(((l-avg)/avg)*100)), 2)
        except:
            continue
    abc = (sorted(vwap_reversal.items(), key=lambda item: item[1]))
    below_vwap = list(abc)[0:10]
    above_vwap = list(abc)[-10:]
    
    
    name_url_dic_above_vwap = {}
    for i in above_vwap:
        key = i[0]
        value_perc = i[1]
        value_url = eq_url_dic[key]
        name_url_dic_above_vwap[key] = [value_perc, value_url]
    

    name_url_dic_below_vwap = {}
    for i in below_vwap:
        key = i[0]
        value_perc = i[1]
        value_url = eq_url_dic[key]
        name_url_dic_below_vwap[key] = [value_perc, value_url]
    
    lis_vwap_reversion = [name_url_dic_above_vwap, name_url_dic_below_vwap]
    
    # print(lis_vwap_reversion)
    
    return lis_vwap_reversion
    

# vwap_reversal()







