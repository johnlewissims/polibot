import requests
import numpy as np
from bs4 import BeautifulSoup
from pytrends.request import TrendReq   
import matplotlib.pyplot as plt
import pandas as pd
pytrend = TrendReq()

iowa = "https://www.realclearpolitics.com/epolls/2020/president/ia/iowa_democratic_presidential_caucus-6731.html" 

page = requests.get(iowa)
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
mysoup = soup.body.find(id="polling-data-full").table
polls = []
rows = mysoup.find_all('tr')
for row in rows:
    d = row.find_all('td')
    if d is not None and len(d) > 0:
        poll_name = d[0].a
        date = d[1]
        buttigieg = d[2]
        sanders = d[3]
        biden = d[4]
        warren = d[5]
        
        
        if poll_name is not None and len(poll_name) > 0:
            dates = date.text.split(' - ')
            year = "2019-"
            start_date = year + dates[0].replace("/", "-")
            end_date = year + dates[1].replace("/", "-")
            tf = start_date + " " + end_date
            
            # Google Trends
            kw_list = ['Buttigieg', 'Sanders', 'Biden', 'Warren']
            pytrend.build_payload(kw_list=kw_list, timeframe='2019-10-10 2019-11-10', geo='US-IA')
            interest_over_time_df = pytrend.interest_over_time()
            #print(interest_over_time_df['Biden'].mean())
            buttigieg_google = interest_over_time_df['Buttigieg'].mean()
            sanders_google = interest_over_time_df['Sanders'].mean()
            biden_google = interest_over_time_df['Biden'].mean()
            warren_google = interest_over_time_df['Warren'].mean()
            
            single_poll = [poll_name.text, date.text, buttigieg.text, sanders.text, biden.text, warren.text, buttigieg_google, sanders_google, biden_google, warren_google]
            polls.append(single_poll)

# Dataset
poll_dataset = pd.DataFrame(polls) 
