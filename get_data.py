import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import numpy as np

url = "https://ung.edu/together/managing-covid"

class Scrape:
    def __init__(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        self.table = soup.find_all('table')
        self.date = []
        self.person = []
        self.campus = []
        self.impact = []
        self.dict = {}

    def get_dates(self):

        date = []
        for tt in self.table[0].find_all('tr')[1:]:
            d = (tt.find_all('td')[0].text)
            date.append(d.replace("/", "-"))

        self.date = date

        return self.date

    def get_person(self):

        person = []
        for tt in self.table[0].find_all('tr')[1:]:
            tmp = tt.find_all('td')[1].text
            if "Student" in tmp:
                person.append("Student")
            else:
                person.append(tmp)
        self.person = person

        return self.person

    def get_campus(self):

        campus = []
        for tt in self.table[0].find_all('tr')[1:]:
            campus.append(tt.find_all('td')[2].text)

        self.campus = campus

        return self.campus

    def get_impact(self):

        impact = []
        for tt in self.table[0].find_all('tr')[1:]:
            impact_txt = tt.find_all('td')[3].text
            if impact_txt == str('Anyone who may have been in contact with '
                                 'the student has been notified, and all '
                                 'health and safety protocols are being '
                                 'followed consistent with Georgia Department ' 
                                 'of Public Health Protocols.'):
                impact.append(1)

            elif impact_txt == str('Anyone who may have been in contact with'
                                   'the employee has been notified, and all'
                                   'health and safety protocols are being'
                                   'followed consistent with Georgia'
                                   'Department of Public Health Protocols.'):
                impact.append(1)
            else:
                impact.append(0)

        self.impact = impact

        return self.impact

    def full_dict(self):
        dates = self.get_dates()
        people = self.get_person()
        campus = self.get_campus()
        impact = self.get_impact()
        lon =  [None] * len(campus)
        lat = [None] * len(campus)
        number = []

        dahl = [34.5278789, -83.9844275]
        oak = [34.2347566, -83.8676613]
        blue = [34.8512143, -84.3388137]
        ocon = [33.866467, -83.4259915]
        cumm = [34.2241064, -84.1085789]
        for i in range(len(campus)):
            if "Oconee Campus" in campus[i]:
                lat[i] = ocon[0]
                lon[i] = ocon[1]
            elif "Gainesville Campus" in campus[i]:
                lat[i] = oak[0]
                lon[i] = oak[1]
            elif "Blue Ridge Campus" in campus[i]:
                lat[i] = blue[0]
                lon[i] = blue[1]
            elif "Cumming Campus" in campus[i]:
                lat[i] = cumm[0]
                lon[i] = cumm[1]
            else:
                lat[i] = dahl[0]
                lon[i] = dahl[1]

        for i in range(len(people)):
            number.append(i)

        self.dict = dict((z[0],list(z[1:])) for z in zip(number, dates, people,
            campus, impact, lat, lon))

        return self.dict

if __name__ == "__main__":
    print(Scrape(url).full_dict())

