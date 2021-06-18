import smtplib as s
import streamlit as st


def placeorder(new):
    st.write("Placing order for ", new)
    sender_email=st.text_input("Enter user gmail: ")
    password=st.text_input(" Enter user Password ",type="password")
    receiver_email=st.text_input("Enter supplier's email: ")
    subject=st.text_input("Enter email subject")
    body=st.text_area("Please enter body")
    if st.button("Send Email"):
        connection=s.SMTP('smtp.gmail.com',587)
        connection.starttls()
        connection.login(sender_email,password)
        message="Subject:{}\n\n{}".format(subject,body)
        connection.sendmail(sender_email,receiver_email,message)
        connection.quit()
        st.success("Email send successfully!")
