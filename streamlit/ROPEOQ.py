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
import forecastdemand as fore
import placeorder as place
def ROPEOQ(username,new):
    usernamemongo = urllib.parse.quote_plus('arsha')
    passwordmongo = urllib.parse.quote_plus('inventory')
    url='mongodb+srv://{}:{}@cluster0.bws9v.mongodb.net/?retryWrites=true&w=majority'.format(usernamemongo,passwordmongo)
    cluster = MongoClient(url)
    db=cluster[username]
    test=db.DailyDemand
    fore.forecast(username,new)
    # Safety Stock

    for i in db.ProductDetails.find({"Product_id":new}):
        lead_time=i['Lead_time']
        ordering_cost=i['Ordering_cost']
        holding_cost=i['Holding_cost']
        starting_stock=i['Starting_stock']
    df = pd.DataFrame(list(test.find({"Product_id":new})))
    #st.write(df)
    del df['_id']
    del df['Product_id']
    df=pd.melt(df, var_name='Date', value_name='Demand')
    std=stdev(df['Demand'])
    safety_stock=std*1.64*math.sqrt(lead_time)
    #st.write("Safety Stock: ",safety_stock)

    # Reorder Point

    today_date=date.today().strftime('%d/%m/%Y')
    val=df.loc[df["Date"]<=today_date]
    array=val['Demand']
    newarray=array[-90:]
    avg_demand=(np.sum(newarray))/90
    forecastdf = pd.DataFrame(list(db.FinalDemand.find({"Product_id":new})))
    del forecastdf['_id']
    del forecastdf['Product_id']
    forecastdf=pd.melt(forecastdf, var_name='Date', value_name='Demand')
    forecastarray=forecastdf['Demand']
    forearray=forecastarray[0:lead_time]
    avg_forecast= sum(forearray)/lead_time
    avg=(avg_demand+avg_forecast)/2
    reorderpoint= (avg*lead_time)+safety_stock
    #st.write("Reorder point: " ,reorderpoint)
    #st.write("Stock:", starting_stock)


    #Economic Order Quantity
    demyear=df['Demand']
    demandperyear= sum(demyear)/(len(demyear)/365)
    eoq=math.sqrt((2*demandperyear*ordering_cost)/holding_cost)
    #st.write("Economic order quantity: ",eoq)


    db.ProductDetails.update({"Product_id":new},{"$set" : {"Reorder_Point":reorderpoint}},upsert=True) 
    db.ProductDetails.update({"Product_id":new},{"$set" : {"Economic_order_quantity":eoq}},upsert=True) 
    db.ProductDetails.update({"Product_id":new},{"$set" : {"Safety_stock":safety_stock}},upsert=True) 
    if starting_stock-reorderpoint<=0:
        db.ProductDetails.update({"Product_id":new},{"$set" : {"Place_order":False}},upsert=True) 
        st.write("Its time to place the order for",new,". Please place the order.")
        







