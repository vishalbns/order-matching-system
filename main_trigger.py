import math
import random
import Match_engine as m_engine
import datetime
from dateutil.relativedelta import *
import time
import saveDataToGSheet

orders = []
order_number = 1

def input_user_order(input_order, orderList):
    print("input order: ")
    print(input_order)
    id = orderList[0]
    category = orderList[1]
    type = orderList[3]
    quantity = orderList[2]
    price = orderList[4]
    time_of_new_order = orderList[5]
    if type=='market' and category=='sell':
        price=0
    elif type=='market' and category=='buy':
        price=math.inf
    orders.append({'id':id,'type':type,'category':category,'price':price,'quantity':quantity, 'time': time_of_new_order})
    print("order number: ")
    global order_number
    print(order_number)
    if(order_number<input_order):
        order_number += 1
    else:
        main_trigger(30)
def main_trigger(no_of_orders, midpoint=200):
    engine = m_engine.MatchingEngine()

    #random order generator
    for i in range(no_of_orders):
        ran_type = ["market"] * 25 + ["limit"] * 75
        type=random.choice(ran_type)
        category = random.choice(["buy", "sell"])
        if type=='limit':
            ranprice = random.gauss(midpoint,10)
            price=round(ranprice - math.fmod(ranprice, 0.05),2)
        if type=='market' and category=='sell':
            price=0
        elif type=='market' and category=='buy':
            price=math.inf
        quantity = random.randint(100,200)
        #get real time
        #orders.append({'id':i,'type':type,'category':category,'price':price,'quantity':quantity})
        time.sleep(0.05)
        now = datetime.datetime.now()
        t = ('%02d:%02d:%02d.%d' % (now.hour, now.minute, now.second, now.microsecond))[:-4]
        orders.append({'id': i, 'type': type, 'category': category, 'price': price, 'quantity': quantity, 'time': t})
    AllOrders = []
    for i in range(len(orders)):
        AllOrders.append([])
        for k,v in orders[i].items():
            if v == math.inf:
                AllOrders[i].append("inf")
            else:
                AllOrders[i].append(v)
    print(AllOrders)
    saveDataToGSheet.Export_AllOrders_To_Sheets(AllOrders)

    #pushing orders into matching engine
    for order in orders:
        order = m_engine.Order(order['id'],
                             order['type'],
                             order['category'],
                             order['price'],
                             order['quantity'])
        engine.process(order)

    #printing all orders accepted
    for order in orders:
        print(order)

    #printing the trades matched
    engine.get_trades()
    engine.cancel()


#main calling function with no.of orders to be randomly generated and no.of user input orders
#main_trigger(10,1)

''' for i in range(input_order):
        id=int(input("Enter the id:"))
        type=input("Enter the type:")
        category=input("Enter the category:")
        if type=='limit':
            price=int(input("Enter the price:"))
        if type=='market' and category=='sell':
            price=0
        elif type=='market' and category=='buy':
            price=math.inf
        quantity=int(input("Enter the quantity:"))
        orders.append({'id':id,'type':type,'category':category,'price':price,'quantity':quantity})'''


#user inputs
''' for i in range(input_order):
        id = orderList[0]
        category = orderList[1]
        type = orderList[3]
        quantity = orderList[2]
        price = orderList[4]
        if type=='market' and category=='sell':
            price=0
        elif type=='market' and category=='buy':
            price=math.inf
        orders.append({'id':id,'type':type,'category':category,'price':price,'quantity':quantity})'''
