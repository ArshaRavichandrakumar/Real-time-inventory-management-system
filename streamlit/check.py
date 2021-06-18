
import matplotlib.pyplot as plt
import streamlit as st
import Sessionstate
import pandas as pd
from datetime import datetime
import pymongo
from pymongo import MongoClient
import urllib.parse
import collections 
import forecastdemand as fore
import ROPEOQ as safe
import placeorder as place
import datetime 
import io
import make_change as make
def data(username,password):
    usernamemongo = urllib.parse.quote_plus('arsha')
    passwordmongo = urllib.parse.quote_plus('inventory')
    url='mongodb+srv://{}:{}@cluster0.bws9v.mongodb.net/?retryWrites=true&w=majority'.format(usernamemongo,passwordmongo)
    cluster = MongoClient(url)
    #client = MongoClient()
    dbnames = cluster.list_database_names()
    pdt_det=[" "]

    if username in dbnames:
        db=cluster[username]
        
        for i in db.ProductDetails.find():
            #db.ProductDetails.update({"Product_id":i['Product_id']},{"$set" : {"Place_order":False}},upsert=True)     
            #db.ProductDetails.update({"Product_id":i['Product_id']},{"$set" : {"Order_place_date":0}},upsert=True) 
            val1=datetime.datetime.now().strftime('%d/%m/%Y')
            if ((i['Starting_stock']-i['Reorder_Point']<=0)and i['Place_order']==False):
                st.write("Alert: Please reorder the product",i['Product_id'])
                if st.button("Place order"):
                    place.placeorder(i['Product_id'])
                if st.button("Confirm order place"):
                    db.ProductDetails.update({"Product_id":i['Product_id']},{"$set" : {"Place_order":True}},upsert=True)     
                    db.ProductDetails.update({"Product_id":i['Product_id']},{"$set" : {"Order_place_date":val1}},upsert=True) 
            
            
            if(i["Place_order"]==True):
                order_date=pd.to_datetime(i['Order_place_date'])+pd.Timedelta(days=i['Lead_time'])
                order_date=order_date.strftime('%d/%m/%Y')
                if(order_date<=val1):
                    st.write("Alert: Your stock for product",i["Product_id"]," has not reached yet please contact the suppliers!!!")
            
            pdt_det.append(i['Product_id'])
        
        #pdt_det = [" ","7000000004","7000000006","7000000010","7000000022","7000000047","7000000056","7000000065","7000000067","7000000071","7000000072","7000000075","7000000079","7000000094","7000000101","7000000107","7000000121","7000000134","7000000137","7000000138","7000000140","7000000144","7000000145","7000000152","7000000157","7000000182","7000000191","7000000202"]
        display = [" ","Add an inventory", "Existing inventory","Remove inventory"]
        val=st.selectbox("Manage inventory",display)
        if val == "Existing inventory":
            new=st.selectbox("Product Details",pdt_det)
            
            ct= db.DailyDemand.count_documents({"Product_id":new})
            if ct!=0:
                task=[" ","Details of the Product","Historical Demand","Add Daily Demand","Forecast Demand","Reorder Point and Economic Order Quantity","Place Order","Make Changes in the inventory","Update if order replenished"]
                diffval=st.selectbox("Task to do",task)
                test=db.DailyDemand
                if diffval== "Details of the Product":
                    for i in db.ProductDetails.find({"Product_id":new}):
                        st.write("Product id:", i['Product_id'])
                        st.write("Purchase cost:", i['Purchase_cost'])
                        st.write("Lead Time:", i['Lead_time'])
                        st.write("Size:", i['Size'])
                        st.write("Selling Price:", i['Selling_price'])
                        st.write("Starting Stock:", i['Starting_stock'])
                        st.write("Holding Cost:",i['Holding_cost'])
                        st.write("Ordering Cost:", i['Ordering_cost'])
                if diffval== "Historical Demand":
                    df = pd.DataFrame(list(test.find({"Product_id":new})))
                    #for i in db.DailyDemand.find({"Product_id":new}):
                    #    df=pd.DataFrame(i)
                    del df['_id']
                    del df['Product_id']                            
                    df=pd.melt(df, var_name='Date', value_name='Demand')
                    st.title("Demand till now")
                    st.write(df)
                    st.title("Plotting demand for last five days")
                    df=df[-5:]
                    df.plot.bar(x='Date', y='Demand', rot=0)
                    plt.show()
                    st.set_option('deprecation.showPyplotGlobalUse', False)
                    st.pyplot()
                if diffval== "Add Daily Demand":
                    default=0
                    da=datetime.date.today().strftime('%d/%m/%Y')
                    st.write(da)
                    demand=st.number_input("Enter today's demand")
                    #today = datetime.strftime(date,'%d/%m/%Y')
                    #today=str(today)
                    if(st.button("Enter")):
                        db.DailyDemand.update({"Product_id":new}, {"$inc": {str(da): demand}},upsert=True)
                        #test.update({"Product_id":new},{"$set" : {str(da):demand}},upsert=False) 
                        for i in db.ProductDetails.find({"Product_id":new}):                                    
                            stock=i["Starting_stock"]
                            stock=float(stock)-demand
                            db.ProductDetails.update({"Product_id":new},{"$set" : {"Starting_stock":stock}},upsert=False) 
                            st.write("Demand entered successfully")
                            fore.forecast(username,new)
                            safe.ROPEOQ(username,new)
                if diffval== "Forecast Demand":
                    fore.forecast(username,new)
                    finaldf = pd.DataFrame(list(db.FinalDemand.find({"Product_id":new})))
                    del finaldf['_id']
                    del finaldf['Product_id']
                    finaldf=pd.melt(finaldf, var_name='Date', value_name='Demand')
                    st.title("Future Demand")
                    st.write(finaldf)
                    
                if diffval=="Reorder Point and Economic Order Quantity":
                    safe.ROPEOQ(username,new)
                    for i in db.ProductDetails.find({"Product_id":new}):
                        st.write("Safety Stock: ",i['Safety_stock'])
                        st.write("Reorder point: " ,i['Reorder_Point'])
                        st.write("Stock:", i['Starting_stock'])
                        st.write("Economic order quantity: ",i["Economic_order_quantity"])

                if diffval=="Place Order":
                    place.placeorder(new)
                    if st.button("Confirm order"):
                        db.ProductDetails.update({"Product_id":new},{"$set" : {"Place_order":True}},upsert=True)     
                        db.ProductDetails.update({"Product_id":new},{"$set" : {"Order_place_date":val1}},upsert=True) 
                if diffval=="Make Changes in the inventory":
                    make.make_change(username,new)
                            
                if diffval=="Update if order replenished":
                    quantity=st.number_input("Enter the quantity replenished")
                    if st.button("Enter"):
                        db.ProductDetails.update({"Product_id":new},{"$inc" : {"Starting_stock":quantity}},upsert=True)
                        st.write("Changes made successfully!!")
                        db.ProductDetails.update({"Product_id":new},{"$set" : {"Place_order":False}},upsert=True)     
                        db.ProductDetails.update({"Product_id":new},{"$set" : {"Order_place_date":0}},upsert=True)
            else:
                
                db.ProductDetails.remove({"Product_id":new})
                st.write("If the collection does not have daily demand,it will be removed from the database.")
        if val== "Add an inventory":
            add_invent = [" ","Add Product Details", "Add Daily Demand"]
            num=st.selectbox("add",add_invent)
            if num== "Add Product Details":
                st.write("Sample format of product details.Please maintain field name as given.")
                st.image("sampledetail.jpg")
                data_file = st.file_uploader("Upload Product Details", type=["csv", "xlsx"])
                if(st.button("Upload")):
                    if data_file:
                        if data_file.name[-3:] == 'csv':
                            df_data = pd.read_csv(io.StringIO(data_file.read().decode('utf-8')), delimiter=',')
                        elif data_file.name[-4:] == 'xlsx':
                            df_data = pd.read_excel(io.StringIO(data_file.read().decode('utf-8')))
                        else:
                            st.write("Incorrect file format")
                    #df_data['Product_id']=df_data['Product_id']
                    for i in df_data['Product_id']:
                        i=str(i)
                    pdt=str(df_data['Product_id'])
                    val=df_data.to_dict('records')
                    count=0
                    for i in db.ProductDetails.find({}):
                        if str(i['Product_id']) in pdt:
                            count=count+1
                    if count ==0:
                        db.ProductDetails.insert_many(val)
                        st.write(" Product inserted successfully. Please add demand history below. If demand history is less the forecasting will be affected")
                        db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Place_order":False}},upsert=True)     
                        db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Order_place_date":0}},upsert=True) 
                        db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Reorder_Point":0}},upsert=True) 
                        db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Economic_order_quantity":0}},upsert=True) 
                        db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Safety_stock":0}},upsert=True) 
                    else:
                        st.write("There are ",count,"products already in the inventory.Please remove duplicates and add again.")
            db.ProductDetails.remove({"Product_id":"0"})
            if num== "Add Daily Demand":
                count=0
                st.write("Please add Product Details first.")
                st.write("\nSample format of product demand. Please maintain format as given.")
                st.image("sampledemand.jpg")    
                demand_file = st.file_uploader("Upload Demand Details", type=["csv", "xlsx"])
                if(st.button("Upload file")):
                
                    if demand_file:
                        if demand_file.name[-3:] == 'csv':
                            df_demand = pd.read_csv(io.StringIO(demand_file.read().decode('utf-8')), delimiter=',')
                        elif demand_file.name[-4:] == 'xlsx':
                            df_demand = pd.read_excel(io.StringIO(demand_file.read().decode('utf-8')))
                        else:
                            st.write("Incorrect file format")
                    for i in df_demand['Product_id']:
                        i=str(i)
                    prdt=str(df_demand['Product_id'])
                    value=df_demand.to_dict('records')
                    for i in db.DailyDemand.find({}):
                        if str(i['Product_id'] )in prdt:
                            count=count+1
                    if count==0:
                        db.DailyDemand.insert_many(value)
                        st.write(" Product inserted successfully. ")
                    else:
                        st.write("The",count," product already exists. Please do not reupload")
                    db.DailyDemand.remove({"Product_id":"0"})
                    
        
                    
                    for i in db.ProductDetails.find({}):
                        if i['Reorder_Point']==0:
                            fore.forecast(username,i['Product_id'])
                            safe.ROPEOQ(username,i['Product_id'])
            

            
            
        if val=="Remove inventory":
            rem=st.selectbox("Product to be removed",pdt_det)
            if st.button("Enter"):
                db.DailyDemand.remove({"Product_id":rem})
                db.ProductDetails.remove({"Product_id":rem})
                db.FinalDemand.remove({"Product_id":rem})
                st.write("Product removed successfully")

    else:
        db=cluster[username]
        add_invent = [" ","Add Product Details", "Add Daily Demand"]
        num=st.selectbox("Add",add_invent)
        if num== "Add Product Details":
            st.write("Sample format of product details.Please maintain field name as given.")
            st.image("sampledetail.jpg")
            data_file = st.file_uploader("Upload Product Details", type=["csv", "xlsx"])
            if(st.button("Upload")):
                if data_file:
                    if data_file.name[-3:] == 'csv':
                        df_data = pd.read_csv(io.StringIO(data_file.read().decode('utf-8')), delimiter=',')
                    elif data_file.name[-4:] == 'xlsx':
                        df_data = pd.read_excel(io.StringIO(data_file.read().decode('utf-8')))
                    else:
                        st.write("Incorrect file format")
                    #df_data['Product_id']=df_data['Product_id']
                for i in df_data['Product_id']:
                    i=str(i)
                pdt=str(df_data['Product_id'])
                val=df_data.to_dict('records')
                count=0
                for i in db.ProductDetails.find({}):
                    if str(i['Product_id']) in pdt:
                        count=count+1
                if count ==0:
                    db.ProductDetails.insert_many(val)
                    st.write(" Product inserted successfully. Please add demand history below. If demand history is less the forecasting will be affected")
                    db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Place_order":False}},upsert=True)     
                    db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Order_place_date":0}},upsert=True) 
                    db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Reorder_Point":0}},upsert=True) 
                    db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Economic_order_quantity":0}},upsert=True) 
                    db.ProductDetails.update({"Product_id":pdt[0]},{"$set" : {"Safety_stock":0}},upsert=True) 
                else:
                    st.write("There are ",count,"products already in the inventory.Please remove duplicates and add again.")
        db.ProductDetails.remove({"Product_id":"0"})
        if num== "Add Daily Demand":
            count=0
            st.write("Please add Product Details first.")
            st.write("\nSample format of product demand. Please maintain format as given.")
            st.image("sampledemand.jpg")    
            demand_file = st.file_uploader("Upload Demand Details", type=["csv", "xlsx"])                
            if(st.button("Upload file")):
                if demand_file:
                    if demand_file.name[-3:] == 'csv':
                        df_demand = pd.read_csv(io.StringIO(demand_file.read().decode('utf-8')), delimiter=',')
                    elif demand_file.name[-4:] == 'xlsx':
                        df_demand = pd.read_excel(io.StringIO(demand_file.read().decode('utf-8')))
                    else:
                        st.write("Incorrect file format")
                for i in df_demand['Product_id']:
                    i=str(i)
                prdt=str(df_demand['Product_id'])
                value=df_demand.to_dict('records')
                for i in db.DailyDemand.find({}):
                    if str(i['Product_id'] )in prdt:
                        count=count+1
                if count==0:
                    db.DailyDemand.insert_many(value)
                    st.write(" Product inserted successfully. ")
                else:
                    st.write("The",count," product already exists. Please do not reupload")
                    db.DailyDemand.remove({"Product_id":"0"})

            

                    