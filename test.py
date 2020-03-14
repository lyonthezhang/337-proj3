import re
# from bs4 import BeautifulSoup
import requests

def testme():
	recipe = '''
			https://www.allrecipes.com/recipe/162760/fluffy-pancakes/
			'''
	html = requests.get(recipe)
	r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")
	return html