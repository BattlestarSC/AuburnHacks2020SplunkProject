from youtube_transcript_api import YouTubeTranscriptApi
import sys
import pafy
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import json
from textblob import TextBlob
import os
import re
import socket
import socketserver
import spacy
from spacy import displacy
from collections import Counter
from bs4 import BeautifulSoup
import urllib.request
import flask
from flask import request, jsonify

import en_core_web_sm
nlp = en_core_web_sm.load()

def loadChannel(channel):
    url = "https://www.youtube.com/channel/" + str(channel)
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    links = []
    for link in soup.find_all('a', href=True):
        if "watch" in str(link['href']):
            links.append("https://youtube.com" + str(link['href']))

    videos_pafy = []
    for link in links:
        videos_pafy.append(pafy.new(str(link)))

def getVideoInfo(video):
    OUTPUT = {}
    OUTPUT['author'] = video.author
    OUTPUT['category'] = video.category
    OUTPUT['desc'] = video.description
    OUTPUT['rating'] = video.rating
    OUTPUT['likes'] = video.likes
    OUTPUT['dislikes'] = video.dislikes
    OUTPUT['duration'] = video.duration
    try:
        OUTPUT['keywords'] = video.keywords
    except:
        OUTPUT['keywords'] = str("None")

    OUTPUT['date'] = video.published
    OUTPUT['video_id'] = video.videoid
    OUTPUT['title'] = video.title
    OUTPUT['views'] = video.viewcount
    OUTPUT['username'] = video.username

    del video

    texts = []
    OUTPUT['raw_text_segments'] = []

    try:
        transcript = YouTubeTranscriptApi.get_transcript(OUTPUT['video_id'])
        # print("!DEBUG: " + str(transcript))
        for dic in transcript:
            # print("!DEBUG: " + str(dic))
            texts.append(dic['text'])
            OUTPUT['raw_text_segments'].append(dic['text'])
    except:
        OUTPUT['raw_text_segments'] = ["FAILED TO GET TRANSCRIPT"]

    ALL_RAW_TEXT = ""
    for tex in texts:
        ALL_RAW_TEXT += str(tex)
        ALL_RAW_TEXT += " "

    # sanatize
    # please never go back and read this, it just shouldn't be done
    texts = [(TextBlob(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tex).split())), tex) for tex in texts]

    ana = lambda textblobobject : "POSITIVE" if (textblobobject.sentiment.polarity > 0) else "NEGATIVE"
    power = lambda textb : abs(textb.sentiment.polarity)

    OUTPUT['sentiment'] = [ {
        "Text": d[1],
        "Sentiment": ana(d[0]),
        "Strength": power(d[0])
    } for d in texts]

    count = lambda s : int(1) if (s == "POSITIVE") else int(-1)
    summation = 0
    for d in OUTPUT['sentiment']:
        value = float(d['Strength']) * float(count(d['Sentiment']))
        summation += value

    OUTPUT['overall_sentiment'] = {
        "Sentiment" : "POSITIVE" if (summation >= 0) else "NEGATIVE",
        "Strength" : abs(summation)
    }


    article = nlp(ALL_RAW_TEXT)
    OUTPUT['all_entities'] = [str(x.text) + "; " for x in article.ents]
    Counter([x.text for x in article.ents]).most_common(3)
    OUTPUT['main_entities'] = str(Counter([x.text for x in article.ents]).most_common(3))

    return OUTPUT

def loadChannel(channel):
    resp = urllib.request.urlopen("https://www.youtube.com/channel/" + str(channel))
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    links = []
    for link in soup.find_all('a', href=True):
        if "watch" in str(link['href']):
            links.append("https://youtube.com" + str(link['href']))

    videos_pafy = []
    for link in links:
        videos_pafy.append(pafy.new(str(link)))

    out = []

    for video in videos_pafy:
        out.append((getVideoInfo(video)))

    return out


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/v1/youtubeTranslator', methods=['GET'])
def api_chan():
    if 'channel' in request.args:
        channel = str(request.args['channel'])
        return jsonify(loadChannel(channel))

app.run()
