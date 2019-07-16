# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 20:37:47 2019

@author: Eric Born
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

#statCols = ['Name', 'WSOP_FT', 'WPT_FT', 'EPT_FT', 'Total tourneys']
#statCols = ['Name', 'WSOP_FT']

# single player
# webpage = requests.get('https://www.cardplayer.com/poker-players/1283-antonio-esfandiari')

# player list view
#webpage = requests.get('https://www.cardplayer.com/poker-players/wsop?page=1')

# May have a response/timeout error when pulling from so many pages in a row
# Use a smaller range if this happens
for i in range(1,201):
    playersDF = pd.DataFrame()
    
    url = 'https://www.cardplayer.com/poker-players/wsop?page='
    webpage = requests.get(url + str(i))

    # Decode the page
    webpageSrc = webpage.content.decode('utf-8')
    
    # conver the page to beautiful soup format
    soup = bs(webpageSrc, 'lxml')

    # Creates an empty list to store all final table counts
    final_tables = []
    
    for x in range(14,309,6):
        final_tables.append(soup.find_all('td')[x])
     
    # Loop that removes <td> and converts the data to a string
    for y in range(len(final_tables)):
        final_tables[y] = int(re.sub(r'<.*?td>', '', str(final_tables[y])))
    
    # Empty list for the player names
    player_name = []    
        
    # Store player names in a list
    for k in soup.find_all('td',{'class':'player-player-name'}):    
        player_name.append(k.text)

    # Checks if the dataframe already has any items in it. 
    # If it does it appends, if not it creates
    if len(playersDF) > 0:
        # Store new gun in second dataframe    
        playersDF2 = pd.DataFrame(list(zip(player_name, final_tables)),
                          columns = ['Name', 'FT'])           
       
        # Append df2 to original df
        playersDF = playersDF.append(playersDF2)      
    else:
        playersDF = pd.DataFrame(list(zip(player_name, final_tables)),
                          columns = ['Name', 'FT'])
    
    playersDF.to_csv('poker.csv', mode='a', header=False)


with open(r'C:\Users\TomBrody\Desktop\School\677\wk1\poker.csv') as f:
    lines = f.read().splitlines()
    #list_lines = lines.split('\n')

win = []

# Inserts the last item in each line, which is the final table apperances.
for line in range(1, len(lines)):
    indices = [i for i, s in enumerate(lines[line]) if ',' in s]
    win.append(int(lines[line][-1]))

def avg(lst):
    return sum(lst) / len(lst)

avg(win)

# Grab item name from the firstHeading
# Single player page
#player_name = soup.find('h1',{'class':'player-name'}).text

#soup.find('td',{'class':'player-player-name'}).text

#print(playersDF.iloc[1,:])
#
#print(playersDF.iloc[:,1])
#
#len(armorDF)
