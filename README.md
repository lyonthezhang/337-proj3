# Conversational Interfaces Project
### Team 13
### Members: Lyon Zhang, David Zane, Christine Garver

It's ok.py

## About OkBot
Okbot is the best sous-chef out there. Okbot can scrape a recipe from Allrecipes.com for you and answer questions about the steps and ingredients while you cook. Just type your question or command and Okbot will answer!

## How to Run OkBot
1. Make sure you are running a conda environment.
2. Run `python ok.py`

## Python Libraries Imported
- import sys
- import fractions
- import copy
- import bs4 from BeautifulSoup
- import requests
- import re
- import random
- from flask import Flask, request
- from pymessenger.bot import Bot
- import os

## Attempt at Connecting to Messenger

We used the following two guides to set up the Flask app connecting to Facebook messenger:

https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html
https://www.twilio.com/blog/2018/02/facebook-messenger-bot-heroku-python-flask.html

The flask ask works perfectly following ONLY the instructions from the first guide and when hosting locally. However, we were unable to successfuly host the bot on a remote server with Heroku due to a multitude of problems (mostly with BeautifulSoup). Here is a screencap showing usage when hosted LOCALLY:

![Conversing with locally hosted messenger OkBot]()

Another thing to note is that the requirements.txt file is NOT for use for running ok.py and was an artifact from linking with Heroku. Please do NOT use it for running ok.py.
