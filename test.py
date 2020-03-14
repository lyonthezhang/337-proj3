import re
from bs4 import BeautifulSoup
import requests

def testme():
	recipe = 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'

	html = requests.get(recipe)
	response = "DUMMY: "
	page_graph = BeautifulSoup(page_html.content)#, features="lxml")
	# page_graph = BeautifulSoup("<head>HEYWHATTHEFUCK</head>")
	return response + str(page_graph)