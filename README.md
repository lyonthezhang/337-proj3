# Recipes Project
#### Team 13
#### Members: Lyon Zhang, David Zane, Christine Garver

We wrote separate python files for each function called in driver.py. We use web scraping to scrape recipes from allrecipes.com and then NLP to find information about the ingredients and directions before transforming the recipe. Users can choose how to transform the recipe using the command line.

## Required Recipe Transformations

## Parse Recipe
To parse the recipe, we created separate lists of keywords to capture cooking method, tools, time, and ingredients. Then, we went through each ingredient and direction the recipe to find matches between the keywords in the lists and the words in the step/ingredient.

### To and From Vegetarian:
To turn the recipe into the vegetarian version, we go through the list of ingredients/directions, and we substitute each meat product with a vegetarian option, such as tofu.
To the turn the recipe into a meat version, we go through the list of ingredients/directions, and we substitute each tofu product with a meat option, such as beef or chicken.
If a vegetarian recipe does not have any main protein, we add chicken to the recipe.

### To and From Healthy:
To turn the recipe into a healthier or unhealthier version, we created a dictionary of ingredients that can be used as substitutions for each other. For example, whole wheat bread is a healthier version of white bread, so we created a key, value pair between whole wheat bread and white bread.
Then we went through each ingredient/direction, and replaced keys with their values.

### Make Italian:

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
