from get_data import Scrape
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import datetime

url = "https://ung.edu/together/managing-covid"

data = Scrape(url).full_dict()

st.title("UNG Confirmed COVID Cases")

st.subheader("Data")
df = pd.DataFrame(data)
df_t = df.transpose()
df_t.columns = ['Date', 'Person', 'Campus', 'Impact', 'latitude', 'longitude']

df_t.time = pd.to_datetime(df_t['Date'], format='%m-%d-%y')
df_t['Date'] = pd.to_datetime(df_t['Date'])
df = df_t.set_index('Date')

st.dataframe(df)

impacts_def = [str('The student has not been on campus for more than two weeks'
                   '; no campus impact'), 
               str('Anyone who may have been in contact with '
               'the student/employee has been notified, and all '
                'health and safety protocols are being '
               'followed consistent with Georgia Department '
               'of Public Health Protocols.')]

impact_df = pd.DataFrame(impacts_def, columns=['Impact Meaning'])

if st.checkbox("Show Impact Definitions"):
    st.subheader("Impact Meanings")
    st.table(impact_df)    

df['day'] = df.index.date
counts = df.groupby(['day']).count()
counts.columns = ['Reported Cases','','','','']
#counts = pd.DataFrame(counts, columns=['count'])

st.bar_chart(counts['Reported Cases'])

if st.checkbox('Show Campus Locations'):
        st.subheader('Campus Locations')
        st.map(df_t)

