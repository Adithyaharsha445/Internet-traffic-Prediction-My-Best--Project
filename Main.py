import streamlit as st
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA 
import datetime
import time
from streamlit_option_menu import option_menu
from PIL import Image

df = pd.read_csv("D:\DeploySourceCode\Data.csv")
df.columns = ['Date','Daily Visitors']
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df = df.set_index('Date')
final_arima = ARIMA(df['Daily Visitors'],order = (3,1,4))

st.title("Internet Traffic Prediction")
with st.sidebar:
    selectUsage = option_menu("Menu", ["Home", 'Present Usage','Forcast Usage'], 
        icons=['house', 'gear','cast'], menu_icon="cast", default_index=0)

with st.container():

    if selectUsage =='Home':
        img = Image.open('D:\DeploySourceCode\home.png')
        st.image(img)
    else:
        st.header(selectUsage)

    if selectUsage == 'Present Usage':
        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(df)
        with col2:
            with st.expander("Present Usage Data"):
                st.dataframe(df,width=500, height=300)

    if selectUsage == 'Forcast Usage':
        forcastdate = datetime.datetime.now()
        st.text("Forcast Date :")
        dt = st.date_input(' ')
        dt =pd.to_datetime(dt)
        if dt < forcastdate:
            st.error('Forcast date must be future date')
        else:
            st.text("Forcast visitor :")
            forcastdate1 = dt.strftime('%Y-%m-%d') + 'T00:00:00'
            modelfit =final_arima.fit().predict(start=forcastdate1,end=forcastdate1)
            with st.spinner('Calculating Forcasting visitor'):
                time.sleep(1)
                st.title("{:.0f}".format(modelfit[0]))
          
    

