import requests
from bs4 import BeautifulSoup
    
page = requests.get('https://www.realclearpolitics.com/epolls/2020/president/ia/iowa_democratic_presidential_caucus-6731.html')
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
        sample = d[2]
        moe = d[3]
        clinton = d[4]
        trump = d[5]
        if poll_name is not None and len(poll_name) > 0:
            single_poll = [poll_name.text, date.text, sample.text, moe.text, clinton.text, trump.text]
            polls.append(single_poll)
print(polls)
