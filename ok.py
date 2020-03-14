import sys
import web_scraping
import human_readable
import parse_recipe


# Valid recipe:
lmao = '''
https://www.allrecipes.com/recipe/162760/fluffy-pancakes/
'''
# Explore recipe:
lmao = '''
https://www.allrecipes.com/recipe/8039/bee-sting-cake-bienenstich-ii/
'''

expletives = ['fart','darn','heck','shut up','stupid','poop']
retrieval_keywords = ['show','get','display','let me see','gimme','give']
enumerations = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelfth']
negation = 'to last'


def remove_punctuation(text):
	text = text.replace(",", "")
	text = text.replace(".", "")
	text = text.replace("-", "")
	return text

def directionNavigator(userinput):
	global res
	global res_index
	global enumerations
	global negation

	counter = 0
	for word in enumerations:
		if word in userinput:
			if negation in userinput:
				res_index = len(res['directions']) - 1 - counter
			else:
				res_index = counter
			print('\nOKBot: {}'.format(res['directions'][res_index]))
			return
		counter += 1
		if counter == len(res['directions']):
			break

	if 'next' in userinput or 'forward' in userinput:
		if res_index >= len(res['directions']):
			print('\nOkBot: No more steps buddy. Congrats!')
			res_index = 0
			return
		res_index += 1
		print('\nOKBot: {}'.format(res['directions'][res_index]))
		return

	if 'back' in userinput or 'previous' in userinput:
		if res_index <= 0:
			print('\nOkBot: Cannot go before the first step, sadly.')
			res_index = 0
			return
		res_index -= 1
		print('\nOKBot: {}'.format(res['directions'][res_index]))
		return

	if 'repeat' in userinput or 'again' in userinput:
		print('\nOKBot: ' + res['directions'][res_index])
		return

	if 'what' in userinput and 'directions' in userinput:
		dir = res['directions']

		print('\nOKBot: Here are the directions:\n')
		for i in range(len(dir)):
			print("Step {}: {}".format(i + 1, dir[i]))
		return

	# print('\nOkBot: Here are the directions:\n')
	# human_readable.print_directions(res, title='')

def parseInput(userinput):
	global res

	parsed_res = parse_recipe.parse_recipe(res)
	userinput = remove_punctuation(userinput.lower())

	ingredients = [x['name'] for x in parsed_res['ingredients']]
	parsed_ingredients = list(map(remove_punctuation, ingredients))
	parsed_ingredients = [x.split() for x in parsed_ingredients]
	ingredients_lst = [item for sublist in parsed_ingredients for item in sublist]

	# ingredients retrieval
	for word in expletives:
		if word in userinput:
			print("\nOkBot: Please don't say bad words, I was born recently and am legally still a child.\n")

	if 'ingredient' in userinput or 'ingredients' in userinput: # and any([x in userinput for x in retrieval_keywords]):
		print('\nOkBot: Here is the ingredients list:\n')
		human_readable.print_ingredients(res, title='')
		return

	if ('direction' in userinput or 'step' in userinput or 'directions' in userinput or 'steps' in userinput):# and any([x in userinput for x in retrieval_keywords]):
		# print('\nOkBot: Here are the directions:\n')
		# human_readable.print_directions(res, title='')
		directionNavigator(userinput)
		return

	# 'how to' questions
	parsed_res = parse_recipe.parse_recipe(res)
	if 'how' in userinput:
		objects = parsed_res['methods'] + parsed_res['tools']
		if any([x in userinput for x in objects]):
			search_base_url = 'https://www.youtube.com/results?search_query=%s'
			search_url = search_base_url % (userinput.replace(' ','+'))
			print('\n' + search_url)
		return

	# 'what is' questions
	if 'what' in userinput:
		objects = parsed_res['tools'] + parsed_res['methods'] + ingredients_lst

		#[x['name'] for x in parsed_res['ingredients']]
		if any([x in userinput for x in objects]):
			search_base_url = 'https://www.google.com/search?q=%s'
			search_url = search_base_url % (userinput.replace(' ','+'))
			print('\n' + search_url)
		return


print("\nOkBot: Hello. I am OkBot. How are you? Please ask me to walk you through a recipe.\n")
userinput = input("User: ")
if 'recipe' or 'cook'  or 'recipes' in userinput:
	print("\nOkBot: Sure thing chicken wing! Please specify a URL.\n")
else:
	print("\nOkBot: I know you didn't ask, but please specify a URL for a recipe anyways. Please don't mess around with me, I'm primitive :)\n")

userinput = input("User: ")
rf = web_scraping.RecipeFetcher()

while True:
	print("\nOkBot: Let me grab that for you...\n")
	try:
		res = rf.scrape_recipe(userinput)
		break
	except:
		print("OkBot: Sorry, my scraper says that's invalid. Someone should fire my developers. Please try another URL.\n")
		userinput = input("User: ")

print("OkBot: Awesome-sauce'em-possum!! Let's proceed with the recipe " + res['name'] + "! What would you like to do with this? You can go over ingredients list or go over recipe steps, or anything else your pure heart desires.")
res_index = -1

while True:
	print("\nOkBot: So what can this humble bot do for you?\n")
	userinput = input("User: ")
	parseInput(userinput)