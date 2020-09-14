#!/usr/bin/env python3
import tweepy
import urllib.request
from bs4 import BeautifulSoup


api_key = "****"
api_key_secret = "****"
access_token = "****"
access_token_secret = "****"

screen_name = "PythonNewQiita"


def get_tweet():
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweet = tweepy.Cursor(api.user_timeline, id=screen_name,
                          tweet_mode="extended").items(1)

    for sentence in tweet:
        url_index = str(sentence.full_text).find("http")
        url = str(sentence.full_text)[url_index:]
    return url


def get_html(url):
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    html = html.read().decode("utf-8")
    return html


def get_url_info(html):
    target = BeautifulSoup(html, "lxml")

    for sentence, url in zip(target.find_all("h1", class_="entry-title"),
                             target.find_all(
            "a", class_="btn btn-primary", href=True)):
        print("qiita: "+sentence.text.strip())
        print("url: ", url['href']+"\n")


def main():
    url = get_tweet()
    html = get_html(url)
    get_url_info(html)


main()
