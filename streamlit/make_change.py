import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datetime import datetime
import pymongo
from pymongo import MongoClient
import urllib.parse
import collections
from itertools import combinations_with_replacement
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cmx
import matplotlib.colors as colors
from statistics import stdev
import numpy as np
import math
import datetime
from datetime import date
def make_change(username,new):
    usernamemongo = urllib.parse.quote_plus('arsha')
    passwordmongo = urllib.parse.quote_plus('inventory')
    url='mongodb+srv://{}:{}@cluster0.bws9v.mongodb.net/?retryWrites=true&w=majority'.format(usernamemongo,passwordmongo)
    cluster = MongoClient(url)
    db=cluster[username]
    
    m_ch=[" ","Lead time","Purchase cost","Size","Selling price","Stock","Holding cost","Ordering cost","Change demand on a particular day"]
    makechange=st.selectbox("Changes to be made",m_ch)
    if makechange=='Lead time':
        ch_lead_time=st.number_input("Enter new lead time")
        if st.button("Enter"):
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Lead_time":int(ch_lead_time)}},upsert=True)
            st.write("Changes made successfully!!")
    if makechange=='Purchase cost':
        ch_purchase_cost=st.number_input("Enter new purchase cost")
        if st.button("Enter"):
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Purchase_cost":ch_purachase_cost}},upsert=True)
            st.write("Changes made successfully!!")
    if makechange=='Size':
        ch_size=st.number_input("Enter new size")
        if st.button("Enter"):
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Size":ch_size}},upsert=True)
            st.write("Changes made successfully!!")
    if makechange=='Selling price':
        ch_selling_price=st.number_input("Enter new selling price")
        if st.button("Enter"):
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Selling_price":ch_selling_price}},upsert=True)
            st.write("Changes made successfully!!")
    if makechange=='Stock':
        ch_stock=st.number_input("Enter new stock")
        if st.button("Enter"):
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Starting_stock":ch_stock}},upsert=True)
            st.write("Changes made successfully!!")
    if makechange=='Holding cost':
        ch_holding_cost=st.number_input("Enter new holding cost")
        if st.button("Enter"):
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Holding_cost":ch_holding_cost}},upsert=True)
            st.write("Changes made successfully!!")

    if makechange=='Ordering cost':
        ch_ordering_cost=st.number_input("Enter new ordering cost")
        if st.button("Enter"):
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Ordering_cost":ch_ordering_cost}},upsert=True)
            st.write("Changes made successfully!!")

    if makechange=='Change demand on a particular day':
        ch_date=st.date_input("Enter the date to make change")
        change_date=ch_date.strftime('%d/%m/%Y')
        ch_demand=st.number_input("Enter new demand")
        if st.button("Enter"):
            for i in db.ProductDetails.find({"Product_id":new}):
                        stock=i["Starting_stock"]
            stock=stock-ch_demand
            db.DailyDemand.update({"Product_id":new},{"$set" : {change_date:ch_demand}},upsert=True)
            db.ProductDetails.update({"Product_id":new},{"$set" : {"Starting_stock":stock}},upsert=False) 
            st.write("Changes made successfully!!")
