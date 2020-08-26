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

#############

# Total number of cases
st.subheader("Total Cases Reported")
st.header(len(data))

#############

# Edit data in pandas dataframe
st.subheader("Data")

@st.cache(allow_output_mutation=True)
def data_table():
    df_og = pd.DataFrame(data)
    df_t = df_og.transpose()
    df_t.columns = ['Date', 'Person', 'Campus', 'Impact', 'latitude', 'longitude']

    # Edit date
    df_t.time = pd.to_datetime(df_t['Date'], format='%m-%d-%y')
    df_t['Date'] = pd.to_datetime(df_t['Date'])
    dataframe = df_t.set_index('Date')
    dataframe['day'] = dataframe.index.date
    return dataframe

def impacts():
    # Set impacts meanings
    impacts_def = [str('The student has not been on campus for more than two weeks'
                       '; no campus impact'), 
                   str('Anyone who may have been in contact with '
                       'the student/employee has been notified, and all '
                       'health and safety protocols are being '
                       'followed consistent with Georgia Department '
                        'of Public Health Protocols.')]

    return pd.DataFrame(impacts_def, columns=['Impact Meaning'])


tmp = data_table()
df1 = tmp.copy(deep=True)


# Show data with out latitude and longitude columns
if st.checkbox("Data Table"):
    st.dataframe(df1.drop(['latitude', 'longitude', 'day'], 1))
    st.subheader("Impact Meanings")
    st.table(impacts())


def graphs(data):
    # Edit data for histogram
    df = data 
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

    fig = px.pie(campus_count.reset_index(), values='Reported Cases',
                 names='Campus')

    st.plotly_chart(fig)

    # Person type distribution
    st.subheader("Employee \ Student Split")
    person_count = df.groupby(['Person']).count()
    person_count.columns = ['Reported Cases','','','','']

    fig1 = px.pie(person_count.reset_index(), values='Reported Cases',
                 names='Person')
    st.plotly_chart(fig1)

graphs(df1)

# Show Campuses on a map
if st.checkbox('Show Campus Locations'):
        st.subheader('Campus Locations')
        st.map(df1)



