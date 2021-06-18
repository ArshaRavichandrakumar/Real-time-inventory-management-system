import check
import streamlit as st
def app():
    import pymongo
    from pymongo import MongoClient
    import urllib.parse
    import collections 
    username = urllib.parse.quote_plus('arsha')
    password = urllib.parse.quote_plus('inventory')
    url='mongodb+srv://{}:{}@cluster0.bws9v.mongodb.net/User_Details?retryWrites=true&w=majority'.format(username,password)
    cluster = MongoClient(url)
    db = cluster['User_Details']
    collection = db['users']
    menu = ["Login","Sign Up"]
    a=[]
    b=[]
    c=[]
    choice = st.sidebar.selectbox("Menu",menu)
    for i in db.users.find({}):
        a.append(i['username'])
        b.append(i['password'])
    if choice == "Login":
        
        username = st.sidebar.text_input("User Name")
            
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            if username in a and password in b:
                check.data(username,password)
            else:
                st.write('Login Failed. If you donot have an account please Sign Up.')
        
    elif choice == "Sign Up":
        
        username = st.text_input("Username")
        Company_name = st.text_input("Company name")
        Phone_number = st.text_input("Phone number")
        Gmail= st.text_input("Company Email id")
        password = st.text_input("Password",type="password")
        confpassword = st.text_input("Confirm Password",type='password')
        if st.button("Submit"):
            if password!=confpassword:
                st.write(" Please check the password you have entered")
            elif username== "" or password == "" or Phone_number== "" or Gmail== "" or Company_name== "" :
                st.write("Please check whether any fields are blank.")
            elif len(username)<=4:
                st.write(" Minimum length of characters needed for username is 4")
            elif len(password)<=8:
                st.write(" Minimum length of characters needed for password is 8")
            elif username in a and password in b:
                st.write("The username and password already exist!! ")
            else:
                record={'username': username,
                    'Company_name' : Company_name,
                    'Phone_number' : Phone_number,
                    'Gmail': Gmail,
                    'password' : password,
                    'confpassword' : confpassword
                    }
                db.users.insert_one(record)
                st.write("Account created successfully")
        
       
            