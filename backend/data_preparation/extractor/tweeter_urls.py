import json
import re

if __name__ == '__main__':

    with open("filteredTweets.json.txt", 'rb') as file:
        data = json.load(file)
        new_dict = dict()
        for item in data:
            id = item["id"]
            text = item["text"]
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

            if urls != []:
                new_dict.update({id: urls})
        print(new_dict)

    json.dump(new_dict, open("tweets_urls.json", "w"))
