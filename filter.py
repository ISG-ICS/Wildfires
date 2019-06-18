# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import pandas as pd
import geopandas as gpd


def NumberOfTweets(data):
    #obtain date    
    Date = []
    for i in data:
        Date.append(i["create_at"][0:10])
    
    #count number of tweets in each day
    count_of_date = {}
    for i in set(Date):
            count_of_date[i] = Date.count(i)
    Date_x = list(count_of_date.keys()) #convert keys in a dictionary to list
    Date_x.sort()
    Count = []
    for i in Date_x:
        Count.append(count_of_date[i])
    
    Date_x = pd.to_datetime(Date_x) #convert string to datetime
    return [Date_x, Count]


def LocationFilter(data):
    # location filter - United States
    data1 = []
    for i in data:
        pointer = i.get('place', None)
        if pointer != None:
            if i['place']['country'] == 'United States':
                data1.append(i)
    return data1


def TimeFilter(data):
    # time filter - 2016-01-01~2017-12-31
    data1 = []
    DateRange = pd.date_range('20160101', '20171231',freq='D')
    DateRange = list(DateRange.strftime('%Y-%m-%d'))
    
    for i in data:
        if i["create_at"][0:10] in DateRange:
            data1.append(i)
    return data1


def RetweetFilter(data):
    # discard retweets
    data1 = []
    for i in data:
        if i['is_retweet'] == False:
            data1.append(i)
    return data1

def RelevanceFilter(data):
    data1 = data[:]
    irelevant_phrase = ['a flood of', 'flooded with', 'flooding back']
    
    for i in data:
        for j in irelevant_phrase:
            if j in i['text']:
                data1.remove(i)
                break
    return(data1)
    
    
def BotFilter(data):
    # discard bot tweets
    data1 = []
    users = []
    botusers = []
    for i in data:
        users.append(i['user']['id'])
    
    count_of_tweets_users = {}
    for i in set(users):
        count_of_tweets_users[i] = users.count(i)
        if count_of_tweets_users[i] > 100:
            botusers.append(i)
    
    for i in data:
        if i['user']['id'] not in botusers:
            data1.append(i)
            
    return data1
    

#open json
with open(r'D:\UCI\Individual Research\data\tweets-flood.json', 'rb') as F:
    data_original = json.load(F)    

#line1
A = []
A = NumberOfTweets(data_original)
x1 = A[0]
y1 = A[1]
# Filter
data_LocationFiltered = LocationFilter(data_original)
data_TimeFiltered = TimeFilter(data_LocationFiltered)
data_RetweetFiltered = RetweetFilter(data_TimeFiltered)
data_BotFiltered = BotFilter(data_RetweetFiltered)
data_RelevanceFiltered = RelevanceFilter(data_BotFiltered)
#line2
A = []
A = NumberOfTweets(data_RelevanceFiltered)
x2 = A[0]
y2 = A[1]


#Figure1&2 - Number of tweets vs Time     
fig = plt.figure(figsize=(20,6))
ax1 = fig.add_subplot(111)
lines1 = ax1.plot(x1,y1,label='$Original Data$')
hl=plt.legend(loc='upper right', frameon=False)

#lines2 = ax1.plot(x2,y2,label='$Filtered Data$')                          
#hl=plt.legend(loc='upper right', frameon=False)

locate=mdate.MonthLocator(range(1, 13), bymonthday=1, interval=2) #set interval to 2 months
ax1.xaxis.set_major_locator(locate) #set major xticks
ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m'))

plt.ylabel('Number of tweets collected')

'''
mondays=mdate.MonthLocator() #obtain the first date of each month
yeardays=YearLocator() # obtain the first date of each year
ax1.xaxis.set_minor_locator(mondays) #set minor xticks
autodates = dt.AutoDateLocator() # display time xaxis automatically
ax.xaxis.set_major_locator(autodates) # set time interval
ax1.set_yscale("log") # set y axis to log axis
'''
# Map  

StateName = []
for i in data_RelevanceFiltered:
    StateName.append(i["geo_tag"]['stateName'])   
count_of_tweets_state = {}
for i in set(StateName):
    count_of_tweets_state[i] = StateName.count(i)
    
shp = gpd.GeoDataFrame.from_file(r'D:\UCI\Individual Research\research\Trial1\map\states.shp')
number_combine = pd.DataFrame.from_dict(count_of_tweets_state, orient='index')
number_combine.columns = ['number of tweets']
map_result = pd.merge(shp, number_combine, left_on='STATE_NAME', right_index=True, how='left', sort=False)


fig, ax = plt.subplots(1, figsize=(30, 40))
map_result['coords'] = map_result['geometry'].apply(lambda x: x.representative_point().coords[:])
map_result['coords'] = [coords[0] for coords in map_result['coords']]
map_result.plot(column='number of tweets', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
ax.axis('off')
for idx, row in map_result.iterrows():
    plt.annotate(s=row['STATE_NAME'], xy=row['coords'], horizontalalignment='center',size=5,color='goldenrod')
#map_result.apply(lambda x: ax.annotate(s=x.STATE_NAME, xy=x.geometry.centroid.coords[0], ha='center'),axis=1)
