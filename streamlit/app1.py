# app1.py
import streamlit as st
import base64
def app():
    main_bg = "sample.jpg"
    main_bg_ext = "jpg"
    side_bg = "sample.jpg"
    side_bg_ext = "jpg"

    #st.markdown(
    #    f"""
    #    <style>
    #    .reportview-container {{
    #        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    #    }}
    #    .sidebar .sidebar-content {{
    #        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    #    }}
    #    </style>
    #    """,
    #    unsafe_allow_html=True
    #)

    original_title = '<p style="font-family:Monsterrat; font-size: 100px;"> INVENTARIO</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="font-family:Monsterrat;font-size: 25px;">  A REAL TIME INVENTORY MANAGEMENT SYSTEM</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    st.write("\n\n")
    
    original_title = '<p style="font-family:Monsterrat; font-size: 35px;">  We uniquely protect you in our deal!</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    st.markdown("""---""")
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 50px;"> Why Inventario? </p>'
    st.markdown(original_title, unsafe_allow_html=True)
    
    original_title = '<p style="font-family:Monsterrat; font-size: 30px;"> If you really want to grow in your business with minimum stress and healthier financial situations, you should think about inventory optimization. Inventario will help you to thrive in the rivalry market. We will ensure safety for your capital with an efficient automated process. </p>'
    st.markdown(original_title, unsafe_allow_html=True)

    st.markdown("""---""")
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 50px;"> Promising service level</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 30px;">If you have the right product on the shelf, you don’t have to worry about the customer service that you could provide. And you should be able to keep an extra layer of inventory then you are never fed up with unsatisfied customer service. Just made a decision about your target service level, Inventario tells you how much you keep in your store.</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 50px;">Reduce inventory level</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 30px;">It is important to reduce the risk due to surplus inventory and cost that comes with capital. With inventario, you could understand the real cost of managing inventory and so you could implement an efficient inventory policy, along with dynamic inventory management discipline.</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 50px;">Automation</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 30px;">Forget inefficient manual processes and free up time to focus on more value adding activities. Inventario provides a tool for automation that allows you to get better handle on demand for your company. Inventario helps to recognize demand patterns and calculates safety stock level, reorder point and economic order quantity.</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    st.markdown("""---""")
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 50px;">ABOUT PRODUCT</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    original_title = '<p style="text-align:left;font-family:Monsterrat;font-size: 30px;">Inventario is an inventory optimization software for demand forecasting based on ERP of your company. The basic features are demand forecasting, inventory planning and inventory replenishment. We are providing an opportunity to get smarter in your business, with tools and insight to improve stock availability with minimum investment.</p>'
    st.markdown(original_title, unsafe_allow_html=True)


    