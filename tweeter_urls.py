import json
import re

with open("tweets-wildfire.json" , 'rb') as file:
    data = json.load(file)
    new_dict =  dict()
    for item in data:
        id = item["id"]
        text = item["text"]
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',text)
        #print("id: "+str(id) + "urls ")
        #print(urls)
        if urls != []:
            new_dict.update({id : urls})
    print(new_dict)

json.dump(new_dict,open("tweets_urls","w"))






