from get_data import Scrape
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import webbrowser
import plotly.express as px
import plotly.graph_objects as go


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
    
    dataframe = df_t.set_index(df_t.time)
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
    d = data_table().set_index('day')
    st.dataframe(d.drop(['latitude', 'longitude', 'Date'], 1))
    st.subheader("Impact Meanings")
    st.table(impacts())


def graphs(data):
    # Edit data for histogram
    df = data 
    counts = df.groupby(['day']).count()
    counts.columns = ['Reported Cases','','','','', '']

    st.subheader("Number Of Reported Cases Each Day")
    st.bar_chart(counts['Reported Cases'])

    st.subheader("Cumulative Case Chart")  
    st.line_chart(counts['Reported Cases'].cumsum())
    plt.plot(counts.cumsum())


    # Campus distribution chart
    st.subheader("Campus Distribution")
    campus_count = df.groupby(['Campus']).count()
    campus_count.columns = ['Reported Cases','','','','','']

    fig = px.pie(campus_count.reset_index(), values='Reported Cases',
                 names='Campus')

    st.plotly_chart(fig)

    # Person type distribution
    st.subheader("Employee \ Student Split")
    person_count = df.groupby(['Person']).count()
    person_count.columns = ['Reported Cases','','','','','']

    fig1 = px.pie(person_count.reset_index(), values='Reported Cases',
                 names='Person')
    st.plotly_chart(fig1)

graphs(df1)

#"""
#df = data_table()
#df1 = df.groupby(['Campus']).count()
#df1.columns = ['Reported Cases','','','','','']
#
#dahl = [34.5278789, -83.9844275]
#oak = [34.2347566, -83.8676613]
#blue = [34.8512143, -84.3388137]
#ocon = [33.866467, -83.4259915]
#cumm = [34.2241064, -84.1085789]

#:wlats = [cumm[0], dahl[0], oak[0], 0, ocon[0]]
#longs = [cumm[1], dahl[1], oak[1], 0, ocon[1]]
#campus_names = ["Cumming", "Dahlonega", "Gainesville", "Oconee"]
#
#df = df1.reset_index()
#
#df["lat"] = lats
#df["lon"] = longs
#
#dff = df.transpose().drop(columns=[3], axis=1)
#df = dff.transpose().set_index("Campus")
#df['text'] = 'Campus: ' + df.index + ' | ' + 'Number of Cases: ' + \
#        df['Reported Cases'].astype(str)
#
#sizes = np.array(df['Reported Cases'])
#
#fig = go.Figure(data=go.Scattergeo(
#                        lon = df['lon'].astype(str),
#                        lat = df['lat'].astype(str),
#                        text = df['text'],
#                        mode = 'markers',
#                        marker_color = df['Reported Cases'],
#                        marker_size = [10, 95, 36, 19]
#                        ))
#
#fig.update_layout(geo_scope='usa')
#
#st.subheader("Campus Bubble Map")
#st.plotly_chart(fig)
#"""



