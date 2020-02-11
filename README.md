# AuburnHacks2020SplunkProject

## Inspiration
My grandmother was interested in judging media opinion and mention of prominent political figures in real time. 

## What it does
This takes lists of youtube channel id's and grabs the videos and transcripts. Every interval of n seconds (default is 3600), the splunk ingest scripts send api requests to a flask api in a docker container. The docker container takes m new videos from each channel, pulls a transcript, and does three pipelines. 
1) video metadata, straight extraction 
2) nlp chunking -> chunk sentiment analysis | This is handled by boxed NLTK algorithms to demonstrate flexibility and ability to perform under non-ideal conditions.
3) named object recognition and tallying | This is handled by boxed scipy algorithms to demonstrate flexibility and ability to perform under non-ideal conditions.
These pipelines are then combined into a python dictionary, transformed into json for the HTML response and interpreted by Splunk.
The goal from this point was to use Splunk dashboards to pull out trends in the data and show a semi-real time graph of the media's presentation of prominent political figures, to get a line graph of how much discussion about them and how positive it is, overall and by outlet. Other trends could and would be pulled out.

## How I built it
Aside from the above mentioned methods, caffeine. 

## Challenges I ran into
Due to the network handling of the pipeline, splunk refused to automatically parse the json leading to over 10 hours of time spent in trying to transform the data into something that could be parsed for the dashboards to be computed on.

## Accomplishments that I'm proud of
Completing the splunk to docker to splunk pipeline functionally (interpretations notwithstanding) and the text processing were major accomplishments for me.

## What I learned
Formatting and API formatting are king. 
My heart needs less caffeine.

## What's next for Live News Sentiment Analysis and Public Opinion Measure
A working demo for a company looking to judge public opinion, to build my skills.

## Current issues.
Python issues with the docker API are documented in that .py file. 
Splunk addon issues: 
-> Due to time, no validation or scheme was made, however this has worked in the past, so I'm assuming its gonna be ok. 
-> The json string returned by the API is being interpreted as a string and no parsed as json. I didn't manage to figure out why before the competition ended. 
