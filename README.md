# Recipes Project
#### Team 13
#### Members: Lyon Zhang, David Zane, Christine Garver

We wrote separate python files for each function called in driver.py. We use web scraping to scrape recipes from allrecipes.com and then NLP to find information about the ingredients and directions before transforming the recipe. Users can choose how to transform the recipe using the command line.

## Required Recipe Transformations

## Parse Recipe
### To and From Vegetarian:
### To and From Healthy
### Make Italian

## Extra Recipe Transformations:

### Make Chinese:
### Double the Amount of Cut it By Half:
### Make Recipe Lactose-Free:
### Make Recipe Spicy:

### How to Run
1. Download and unzip folder.
2. Make sure you have set up a conda environment and it is running.
3. Pick a url of recipe to transform from 'allrecipes.com' or you can use our default recipe:
4. Run `python driver.py <url>` to get the information about the different kinds of transformations.
5. Pick you transformation using command line!

### Python Libraries Imported:
- from bs4 import BeautifulSoup
- import requests
- import re
- import sys
- import fractions

### Websites Used for Reference:
- https://www.allrecipes.com/
- https://www.thekitchn.com/quick-guide-to-every-herb-and-spice-in-the-cupboard-108770
