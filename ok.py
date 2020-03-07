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

expletives = ['fart']
retrieval_keywords = ['show','get','display','let me see','gimme','give']

def directionNavigator(userinput):
	global res
	global res_index

	if 'next' in userinput or 'forward' in userinput:
		print(res['directions'][res_index])
		res_index += 1
		if res_index >= len(res['directions']):
			print('\nOkBot: No more steps buddy. COngrats')
			res_index = 0

	if 'back' in userinput or 'previous' in userinput:
		print(res['directions'][res_index])
		res_index -= 1
		if res_index < 0:
			print('\nOkBot: That was the first step again.')
			res_index = 0

	if 'repeat' in userinput or 'again' in userinput:
		print(res['directions'][res_index])

	# print('\nOkBot: Here are the directions:\n')
	# human_readable.print_directions(res, title='')

def parseInput(userinput):
	global res

	userinput = userinput.lower()

	# ingredients retrieval
	if 'ingredient' in userinput:# and any([x in userinput for x in retrieval_keywords]):
		print('\nOkBot: Here is the ingredients list:\n')
		human_readable.print_ingredients(res, title='')
		return

	if ('direction' in userinput or 'step' in userinput):# and any([x in userinput for x in retrieval_keywords]):
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
			print(search_url)
		return

	# 'what is' questions
	if 'what' in userinput:
		objects = parsed_res['tools'] + parsed_res['methods'] + [x['name'] for x in parsed_res['ingredients']]
		if any([x in userinput for x in objects]):
			search_base_url = 'https://www.google.com/search?q=%s'
			search_url = search_base_url % (userinput.replace(' ','+'))
			print(search_url)
		return


print("\nOkBot: Hello. I am OkBot. How are you? Please ask me to walk you through a recipe.\n")
userinput = input("User: ")
if 'recipe' in userinput:
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

print("OkBot: Awesome-sauce'em-possum!! Let's proceed with the recipe " + res['name'] + "! What would you like to do with this? You can go over ingredients list or go over recipe steps, or anything else your pure heart desires.\n")
res_index = 0

while True:
	print("\nOkBot: So what can this humble bot do for you?\n")
	userinput = input("User: ")
	parseInput(userinput)






