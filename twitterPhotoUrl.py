import requests
import json
import re
import urllib.request
from bs4 import BeautifulSoup
def getTwitterImage(link):
    if requests.get(link).status_code < 400:
        source = urllib.request.urlopen(expandedUrl).read()
        soup = BeautifulSoup(source,'html.parser')
        imgs = soup.findAll("div",{"class":"AdaptiveMedia-photoContainer js-adaptive-photo" })
        imgUrl = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',str(imgs))
        uniqueImgUrl= list(set(imgUrl))
        return uniqueImgUrl
    else:
        #print("404 not found")
        return -1

with open("tweets_urls" , 'rb') as file:
    data = json.load(file)
    tweetPhoto_dict = dict() #this dictionary stores id: url that contains tweets that have pics
    cnt = 0
    for id, item in data.items():
        print(cnt)
        cnt += 1
        for element in item:
            expandedUrl = requests.get(element).url
            #print("expandedUrl is: " + expandedUrl)
            #in the situation that the url links to a tweet with image
            if (expandedUrl.find("twitter")!=-1)and(expandedUrl.find("photo")!=-1):
                #print("the url links to a tweet with photo")
                photoUrl = getTwitterImage(expandedUrl)
                if photoUrl != -1:
                    tweetPhoto_dict.update({id:photoUrl})

            #else:
                #print("the url does NOT link to a tweet with photo")
        if cnt == 200:
            break

    print(tweetPhoto_dict)
json.dump(tweetPhoto_dict,open("tweetPhoto_urls","w"),separators=(',\n', ': '))

