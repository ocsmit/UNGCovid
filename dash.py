from get_data import Scrape
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import webbrowser
import altair as alt
import plotly.express as px


url = "https://ung.edu/together/managing-covid"

data = Scrape(url).full_dict()

# Title
st.title("UNG Confirmed COVID Cases")

st.write('This is a tracking app for the University of North Georgia that '
         'aims to present the data in a more useful manner than that provided '
         'by the university by scraping their web table, processing the data, '
         'and outputting it here.')

# Sidebar links

if st.sidebar.button('UNG Data Site'):
    webbrowser.open_new_tab(url)

if st.sidebar.button('Github'):
    webbrowser.open_new_tab('https://github.com/ocsmit/UNGCovid')

# Total number of cases
st.subheader("Total Cases Reported")
st.header(len(data))

# Edit data in pandas dataframe
st.subheader("Data")
df = pd.DataFrame(data)
df_t = df.transpose()
df_t.columns = ['Date', 'Person', 'Campus', 'Impact', 'latitude', 'longitude']

# Edit date
df_t.time = pd.to_datetime(df_t['Date'], format='%m-%d-%y')
df_t['Date'] = pd.to_datetime(df_t['Date'])
df = df_t.set_index('Date')

# Show data with out latitude and longitude columns
st.dataframe(df.drop(['latitude', 'longitude'], 1))

# Set impacts meanings
impacts_def = [str('The student has not been on campus for more than two weeks'
                   '; no campus impact'), 
               str('Anyone who may have been in contact with '
               'the student/employee has been notified, and all '
                'health and safety protocols are being '
               'followed consistent with Georgia Department '
               'of Public Health Protocols.')]

# Show impacts meanings
impact_df = pd.DataFrame(impacts_def, columns=['Impact Meaning'])

if st.checkbox("Show Impact Definitions"):
    st.subheader("Impact Meanings")
    st.table(impact_df)

# Edit data for histogram
df['day'] = df.index.date
counts = df.groupby(['day']).count()
counts.columns = ['Reported Cases','','','','']

st.subheader("Number Of Reported Cases Each Day")
st.bar_chart(counts['Reported Cases'])

st.subheader("Cumulative Case Chart")  
st.line_chart(counts['Reported Cases'].cumsum())
plt.plot(counts.cumsum())


# Campus distribution chart
st.subheader("Campus Distribution")
campus_count = df.groupby(['Campus']).count()
campus_count.columns = ['Reported Cases','','','','']

campus_count['Reported Cases'].plot(kind='barh')

fig = px.pie(campus_count.reset_index(), values='Reported Cases',
names='Campus')

st.plotly_chart(fig)

# Show Campuses on a map
if st.checkbox('Show Campus Locations'):
        st.subheader('Campus Locations')
        st.map(df_t)



