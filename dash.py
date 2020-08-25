from get_data import Scrape
import streamlit as st
import pandas as pd
import numpy as np


url = "https://ung.edu/together/managing-covid"

data = Scrape(url).full_dict()

st.title("UNG Confirmed COVID Cases")

st.write("Data")
df = pd.DataFrame(data)
df_transposed = df.transpose()
#df_transposed.insert(["Lat", "Long"])
st.write(df_transposed)


dahl = [34.5278789, -83.9844275]
dahl

for i in range(len(data)):
    if data[i][2] == "Dahlonega Campus":
        data[i].append(dahl[0])
        data[i].append(dahl[1])
        print(data)
