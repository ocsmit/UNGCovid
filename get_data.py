import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import numpy as np

url = "https://ung.edu/together/managing-covid"
#page = requests.get(URL)

#soup = BeautifulSoup(page.content, 'html.parser')
#table = soup.find_all('table')


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
            date.append(tt.find_all('td')[0].text)

        self.date = date

        return self.date

    def get_person(self):

        person = []
        for tt in self.table[0].find_all('tr')[1:]:
            person.append(tt.find_all('td')[1].text)

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
            impact.append(tt.find_all('td')[3].text)
        
        impact1 = "Anyone who may have been in contact with the student \
                   has been notified, and all health and safety protocols \
                   are being followed consistent with Georgia Department \
                   of Public Health Protocols."



        impact_class = []
        #for i in range(len(impact)):
        #    if impact[i] == impact1:
        #        impact_class[i].append(2)
        #    else:
        #        impact_class[i].append(1)

        self.impact = impact

        return self.impact

    def full_dict(self):
        dates = self.get_dates()
        people = self.get_person()
        campus = self.get_campus()
        impact = self.get_impact()
        number = []
        for i in range(len(people)):
            number.append(i)

        self.dict = dict((z[0],list(z[1:])) for z in zip(number, dates, people,
            campus, impact))

        return self.dict

if __name__ == "__main__":
    print(Scrape(url).full_dict())

