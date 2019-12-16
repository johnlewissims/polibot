import requests
import numpy as np
from bs4 import BeautifulSoup
from pytrends.request import TrendReq   
import matplotlib.pyplot as plt
import pandas as pd
pytrend = TrendReq()

iowa = "https://www.realclearpolitics.com/epolls/2020/president/ia/iowa_democratic_presidential_caucus-6731.html" 
kw_list = ['Buttigieg', 'Sanders', 'Biden', 'Warren']

page = requests.get(iowa)
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
mysoup = soup.body.find(id="polling-data-full").table
polls_list = []
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
        
            fixed_start = pd.to_datetime(start_date, format='%Y-%m-%d').date()
            fixed_end = pd.to_datetime(end_date, format='%Y-%m-%d').date()
            if fixed_start < fixed_end:
                string_start = fixed_start.strftime("%Y-%m-%d")
                string_end = fixed_end.strftime("%Y-%m-%d")
                
                tf = string_start + " " + string_end
                single_poll = [poll_name.text, tf, buttigieg.text, sanders.text, biden.text, warren.text]
                polls_list.append(single_poll)

# Google Trends
for i in range(len(polls_list)):
    pytrend.build_payload(kw_list=kw_list, timeframe=polls_list[i][1], geo='US-IA')
    interest_over_time_df = pytrend.interest_over_time()
    buttigieg_google = interest_over_time_df['Buttigieg'].mean()
    sanders_google = interest_over_time_df['Sanders'].mean()
    biden_google = interest_over_time_df['Biden'].mean()
    warren_google = interest_over_time_df['Warren'].mean()
    polls_list[i].extend([buttigieg_google, sanders_google, biden_google, warren_google])

# Dataset Evaluation
poll_dataset = pd.DataFrame(polls_list) 

# Flat Linear Regression
X_original = poll_dataset[2].append([poll_dataset[3], poll_dataset[4], poll_dataset[5]]).reset_index(drop=True)
y_original = poll_dataset[6].append([poll_dataset[7], poll_dataset[8], poll_dataset[9]]).reset_index(drop=True)
flat_dataset_original = pd.concat([X_original, y_original], axis=1)
flat_dataset_original = flat_dataset_original.drop([26, 27])
flat_dataset_original[0] = flat_dataset_original[0].astype(int)

flat_dataset = flat_dataset_original.sort_values(by=0)
plt.scatter(flat_dataset_original[0], flat_dataset_original[1], color = 'red')

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

X_train = flat_dataset_original[0].values.reshape(-1,1)
y_train = flat_dataset_original[1].values.reshape(-1,1)

# Actual Data v. Regression CHart
regressor.fit(X_train, y_train)
plt.scatter(X_train, y_train, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')


















