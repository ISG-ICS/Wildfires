from enum import Enum, auto

import requests
import rootpath

rootpath.append()

from utilities.decorators import timeout


class MediaURL(Enum):
    TWEET_IMAGE = auto()
    TWEET_VIDEO = auto()
    INS = auto()
    OTHERS = auto()


class URLClassifier:

    @staticmethod
    @timeout(5)
    def classify(short_link) -> MediaURL:
        # function returns the type of the link, 3 is tweet, 4 is ins, 5 is others
        expanded_url = requests.get(short_link).url
        if expanded_url.find("twitter") != -1 and expanded_url.find("instagram") == -1:
            if expanded_url.find("video") != -1:
                return MediaURL.TWEET_VIDEO
            else:
                return MediaURL.TWEET_IMAGE
        elif expanded_url.find("instagram") != -1:
            return MediaURL.INS
        else:
            return MediaURL.OTHERS
