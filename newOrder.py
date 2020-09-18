#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 22:05:51 2020

@author: vishalbns
"""
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
import dummy_stock_market as dsm
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

lastclose = str(dsm.last_close[0])
openprice = str(dsm.open_price[0])
volume = str(dsm.volume[0])
highprice = str(dsm.highprice[0])
lowprice = str(dsm.lowprice[0])
#AllRealTimeData = lastclose + ' ' + openprice+ ' ' + volume+ ' ' + highprice+ ' ' + lowprice
AllRealTimeData = {"lastclose": lastclose,"openprice":openprice,"volume":volume,"highprice":highprice,"lowprice":lowprice}
print(AllRealTimeData)

from datetime import datetime
import saveDataToGSheet
import main_trigger
from flask import request, redirect, Flask, render_template
app = Flask(__name__)

def index():
    return render_template('index.html')

number_of_user_orders = 1
keyList = ["ordertype", "quantity", "pricetype", "price"]
orderDict = {key: [] for key in keyList}

@app.route('/realtimedata', methods = ['GET', 'POST'])
def get():
    if request.method == 'GET':
        return  jsonify(AllRealTimeData)

@app.route('/clearGsheet', methods = ['GET', 'POST'])
def clear_google_sheets():
    saveDataToGSheet.clear_g_sheets()
    return render_template('index.html')

@app.route('/numUserOrders', methods = ['GET', 'POST'])
def fixnumusers():
    main_trigger.orders = []
    main_trigger.order_number = 1
    if request.method == 'POST':
        global number_of_user_orders
        number_of_user_orders = int(request.form['number_of_user_orders'])
        print("number of user orders: ")
        print(number_of_user_orders)
    return render_template('index.html')

@app.route('/', methods = ['GET', 'POST'])

def newOrder():
    if request.method == 'POST': 
        orderDict["ordertype"].append(request.form['buyorsell'])
        orderDict["quantity"].append(float(request.form['quantity']))
        orderDict["pricetype"].append(request.form['pricetype'])
        orderDict["price"].append(float(request.form['price']))
        #print(orderDict)
        newList = [request.form['buyorsell'], float(request.form['quantity']), request.form['pricetype'],float(request.form['price']), datetime.now().strftime("%H:%M:%S.%f")[:-4]]
        global number_of_user_orders
        print("number of user orders: ")
        print(number_of_user_orders)
        saveDataToGSheet.Export_Data_To_Sheets(newList, number_of_user_orders)
    return render_template('index.html')




if(__name__) == '__main__':
    app.run(debug=True)
