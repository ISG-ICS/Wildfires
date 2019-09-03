import logging
import re
import traceback
import urllib.request
from typing import Union, List, Dict

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from classifiers.url_classifier import URLClassifier, MediaURL
from .extractorbase import ExtractorBase

logger = logging.getLogger('TaskManager')


class TweetMediaExtractor(ExtractorBase):
    HTTP_REGEX = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def extract(self, text: str) -> Union[List, Dict]:
        handlers = {MediaURL.TWEET_IMAGE: self._get_twitter_image, MediaURL.INS: self._get_ins,
                    MediaURL.TWEET_VIDEO: self._get_twitter_video, MediaURL.OTHERS: lambda x: []}
        short_urls = re.findall(self.HTTP_REGEX, text)
        result_urls = list()
        for short_url in short_urls:
            link_type: MediaURL = URLClassifier.classify(short_url)
            result_urls += handlers[link_type](short_url)
        logger.info(f"extracting {short_urls}, results = {result_urls}")
        return result_urls

    def _get_twitter_image(self, url: str) -> List[str]:
        # gets twitter image url
        if requests.get(url).status_code < 300:
            source = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(source, 'html.parser')
            img_div_html = soup.findAll("div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo"})
            img_url = re.findall(self.HTTP_REGEX, str(img_div_html))
            return list(set(img_url))
        return list()

    def _get_twitter_video(self, url: str) -> List:

        driver = webdriver.PhantomJS()
        driver.get(url)
        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        if requests.get(url).status_code < 300:
            soup = BeautifulSoup(html, 'html.parser')
            imgs = soup.find_all("meta")
            img_urls = re.findall(self.HTTP_REGEX, str(imgs))

            img_url = [url for url in img_urls if
                       "facebook" in url]  # twitter video links usually have keyword "facebook"
            return list(set(img_url))
        return list()

    def _get_ins(self, link):
        # gets ins image or video url
        try:
            response = requests.get(link)
            if response.status_code < 300:
                all_urls = re.findall(self.HTTP_REGEX, response.text)
                all_urls_unique = set(all_urls)
                img_urls = [url for url in all_urls_unique if  # ins image
                            "https://scontent-lax3-1.cdninstagram.com" and "e35" in url and "s150x150" not in url]
                if not img_urls:
                    img_urls = [url for url in all_urls_unique if  # ins video
                                "https://scontent-lax3-1.cdninstagram.com" and "mp4" in url and "s150x150" not in url]
                return [img_urls[0]]
            else:
                logger.error('invalid url: ' + str(response.status_code))
                return list()
        except Exception:
            logger.error('error: ' + traceback.format_exc())
            return list()

    def export(self, file_type: str, file_name: str) -> None:
        # not implementing
        pass


if __name__ == '__main__':
    urls = TweetMediaExtractor().extract("Wildfire smoke #okwx https://t.co/zBwGOHVCjU")
    print(urls)
