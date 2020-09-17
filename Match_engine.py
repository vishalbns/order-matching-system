from collections import deque
import threading
from bisect import bisect_right
import math
import saveDataToGSheet

class Order:

    def __init__(self, id, order_type, category, price, quantity):
        self.id = id
        self.type = order_type
        self.category = category.lower()
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return "[" + str(self.price) + " for " + str(self.quantity) + " shares]"

class Trade:

    def __init__(self, buyer, seller, price, quantity):
        self.buy_order_id = buyer
        self.sell_order_id = seller
        self.price = price
        self.quantity = quantity

    def show(self):
        print("[", self.price, self.quantity, "]")


class OrderBook:

    def __init__(self):
        self.bids = []
        self.asks = []


    def add(self,order):

        if (order.category=="buy"):
            self.bids = sorted(self.bids,key=lambda order:-order.price)
            key1 = [-order.price for order in self.bids]
            self.insert(self.bids,key1,order,key=lambda order:-order.price)
        if (order.category=="sell"):
            self.asks = sorted(self.asks,key=lambda order:order.price)
            key2 = [order.price for order in self.asks]
            self.insert(self.asks,key2,order,key=lambda order:order.price)


    def insert(self,lists, keys, new_order, key=lambda v:v):
        k = key(new_order)  
        i = bisect_right(keys,k)  
        keys.insert(i,k)  
        lists.insert(i,new_order)


    def best_bid(self):
        if len(self.bids) > 0:
            return self.bids[0].price
        else:
            return 0

    def best_ask(self):
        if len(self.asks) > 0:
            return self.asks[0].price
        else:
            return 0


    def remove(self,order):
        if order.category == 'buy':
            self.bids.remove(order)
        elif order.category == 'sell':
            self.asks.remove(order)


class MatchingEngine:
    global executedTrades
    global tradeID
    global cancelledTrades

    def __init__(self):
        self.queue = deque()
        self.orderbook = OrderBook()
        self.trades = deque()

    def process(self,order):
        self.match_order(order)


    def get_trades(self):
        executedTrades = []
        tradeID = 0
        for trade in self.trades:
            print(trade.buy_order_id,trade.sell_order_id,trade.price,trade.quantity)
            executedTrades.append([])
            executedTrades[len(executedTrades)-1].append(tradeID)
            executedTrades[len(executedTrades)-1].append(trade.buy_order_id)
            executedTrades[len(executedTrades)-1].append(trade.sell_order_id)
            executedTrades[len(executedTrades)-1].append(trade.price)
            executedTrades[len(executedTrades)-1].append(trade.quantity)
            tradeID = tradeID + 1
        print(executedTrades)
        saveDataToGSheet.Export_ExecutedTrades_To_Sheets(executedTrades)

    def cancel(self):
        cancelledTrades = []
        for i in range(len(self.orderbook.bids)):
            if(self.orderbook.bids[i].price == 'Infinity'):
                self.orderbook.bids[i].price = 0
            print('cancelled bids:')
            print(self.orderbook.bids[i].id,self.orderbook.bids[i].type,self.orderbook.bids[i].category,self.orderbook.bids[i].price,self.orderbook.bids[i].quantity)
            cancelledTrades.append([])
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.bids[i].id)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.bids[i].type)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.bids[i].category)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.bids[i].price)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.bids[i].quantity)

        for i in range(len(self.orderbook.asks)):
            if(self.orderbook.asks[i].price == 'Infinity'):
                self.orderbook.asks[i].price = 0
            print("cancelled asks: ")
            print(self.orderbook.asks[i].id,self.orderbook.asks[i].type,self.orderbook.asks[i].category,self.orderbook.asks[i].price,self.orderbook.asks[i].quantity)
            cancelledTrades.append([])
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.asks[i].id)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.asks[i].type)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.asks[i].category)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.asks[i].price)
            cancelledTrades[len(cancelledTrades)-1].append(self.orderbook.asks[i].quantity)
        print(cancelledTrades)
        saveDataToGSheet.Export_CancelledTrades_To_Sheets(cancelledTrades)


    def match_order(self,order):
        if order.category == 'buy' and order.price >= self.orderbook.best_ask():
            # Buy order crossed the spread
            filled = 0
            consumed_asks = []
            for i in range(len(self.orderbook.asks)):
                ask = self.orderbook.asks[i]

                if ask.price==0 and order.price==math.inf:
                    break
                if ask.price > order.price:
                    break  # Price of ask is too high, stop filling order
                elif filled == order.quantity:
                    break  # Order was filled

                if filled + ask.quantity <= order.quantity:  # order not yet filled, ask will be consumed whole
                    filled += ask.quantity
                    if ask.price == 0:
                        trade = Trade(order.id,ask.id,order.price,ask.quantity)
                    else:
                        trade = Trade(order.id,ask.id,ask.price,ask.quantity)
                    self.trades.append(trade)
                    consumed_asks.append(ask)
                elif filled + ask.quantity > order.quantity:  # order is filled, ask will be consumed partially
                    volume = order.quantity - filled
                    filled += volume
                    if ask.price == 0:
                        trade = Trade(order.id,ask.id,order.price,volume)
                    else:
                        trade = Trade(order.id,ask.id,ask.price,volume)
                    self.trades.append(trade)
                    ask.quantity -= volume

            for ask in consumed_asks:
                self.orderbook.remove(ask)

            if filled < order.quantity:
                self.orderbook.add(Order(order.id,order.type,order.category,order.price,order.quantity - filled))

        elif order.category == 'sell' and order.price <= self.orderbook.best_bid():
            # Sell order crossed the spread
            filled = 0
            consumed_bids = []
            for i in range(len(self.orderbook.bids)):
                bid = self.orderbook.bids[i]

                if order.price==0 and bid.price==math.inf:
                    break
                if bid.price < order.price:
                    break  # Price of bid is too low, stop filling order
                if filled == order.quantity:
                    break  # Order was filled

                if filled + bid.quantity <= order.quantity:  # order not yet filled, bid will be consumed whole
                    filled += bid.quantity
                    if bid.price == math.inf:
                        trade = Trade(bid.id,order.id,order.price,bid.quantity)
                    else:
                        trade = Trade(bid.id,order.id,bid.price,bid.quantity)
                    self.trades.append(trade)
                    consumed_bids.append(bid)
                elif filled + bid.quantity > order.quantity:  # order is filled, bid will be consumed partially
                    volume = order.quantity - filled
                    filled += volume
                    if bid.price == math.inf:
                        trade = Trade(bid.id,order.id,order.price,volume)
                    else:
                        trade = Trade(bid.id,order.id,bid.price,volume)
                    self.trades.append(trade)
                    bid.quantity -= volume

            for bid in consumed_bids:
                self.orderbook.remove(bid)

            if filled < order.quantity:
                self.orderbook.add(Order(order.id,order.type,order.category,order.price,order.quantity - filled))

        else:
            # Order did not cross the spread, place in order book
            self.orderbook.add(order)

    def cancel_order(self,cancel):
        pass