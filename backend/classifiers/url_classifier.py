import requests
import rootpath

rootpath.append()

from utilities.decorators import timeout


class URLClassifier:
    TWEET_IMAGE = 0
    TWEET_VIDEO = 1
    INS = 2
    OTHERS = 3

    @timeout(5)
    def classify(self, short_link):
        # function returns the type of the link, 3 is tweet, 4 is ins, 5 is others
        expanded_url = requests.get(short_link).url
        if expanded_url.find("twitter") != -1 and expanded_url.find("instagram") == -1:
            if expanded_url.find("video") != -1:
                return URLClassifier.TWEET_VIDEO
            else:
                return URLClassifier.TWEET_IMAGE
        elif expanded_url.find("instagram") != -1:
            return URLClassifier.INS
        else:
            return URLClassifier.OTHERS
