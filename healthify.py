import sys
import web_scraping
from healthify_subs import healthy_subs, unhealthy_subs

def healthify(recipe):
	directions = recipe['directions']
	ingredients = recipe['ingredients']
	sub_keys = healthy_subs.keys()

	i = 0
	for base_ing in ingredients:
		for sub_ing in sub_keys:
			if sub_ing in base_ing:
				ingredients[i] = ingredients[i].replace(sub_ing, healthy_subs[sub_ing])
		i += 1

	i = 0
	for step in directions:
		for sub_ing in sub_keys:
			if sub_ing in step:
				directions[i] = directions[i].replace(sub_ing, healthy_subs[sub_ing])
		i += 1

	return directions, ingredients

def unhealthify(recipe):
	directions = recipe['directions']
	ingredients = recipe['ingredients']
	sub_keys = unhealthy_subs.keys()

	i = 0
	for base_ing in ingredients:
		for sub_ing in sub_keys:
			if sub_ing in base_ing:
				ingredients[i] = ingredients[i].replace(sub_ing, unhealthy_subs[sub_ing])
		i += 1

	i = 0
	for step in directions:
		for sub_ing in sub_keys:
			if sub_ing in step:
				directions[i] = directions[i].replace(sub_ing, unhealthy_subs[sub_ing])
		i += 1

	return directions, ingredients


if __name__ == "__main__":
	if len(sys.argv) == 3:
		url = sys.argv[1]
		if url == 'default':
			url = 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'
		rf = web_scraping.RecipeFetcher()
		res = rf.scrape_recipe(url)
		if sys.argv[2] == '0':
			healthify(res)
		else:
			unhealthify(res)
	else:
		print("Invalid Number of Arguements. Run by typing 'python3 driver.py a_url'\n")
