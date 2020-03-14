import re
# from bs4 import BeautifulSoup
import requests

def testme():
	recipe = '''
			https://www.allrecipes.com/recipe/162760/fluffy-pancakes/
			'''
	html = requests.get(recipe)
	response = "DUMMY: "
	return response