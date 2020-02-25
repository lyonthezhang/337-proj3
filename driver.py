import sys
import web_scraping
import multiply_recipe

'''
Driver script to run recipe parsing & transformation interaction with user.
Run by typing 'python3 driver.py a_url' or 'python3 driver.py default'.
The default url is 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'
'''


def main(url):

	print('Your URL:')
	print(url, '\n')

	# parse recipe and print
	rf = web_scraping.RecipeFetcher()
	res = rf.scrape_recipe(url)
	print('Parsed Recipe:')
	print(res, '\n')

	# ask user to select a transformation
	transformations = ['To and from vegetarian (REQUIRED)', 'To and from healthy (REQUIRED)', 'Style of cuisine (AT LEAST ONE REQUIRED)', 'Additional Style of cuisine (OPTIONAL)', 'DIY to easy (OPTIONAL)', 'Double the amount or cut it by half (OPTIONAL)', 'Cooking method (OPTIONAL)']
	num_transformations = len(transformations)
	while True:
		for i in range(num_transformations):
			print(f'{i}) {transformations[i]}')
		selection = input(f'Select a transformation (integer between 0 and {num_transformations - 1}): ')
		print()
		if selection in [str(x) for x in range(num_transformations)]:
			selection = int(selection)
			print(f'You selected: {transformations[selection]} \n')
		else:
			print('Invalid selection. Please try again...\n')
			continue

		# execute user-selected transformation
		if selection == 0:
			pass
		elif selection == 1:
			pass
		elif selection == 2:
			pass
		elif selection == 3:
			pass
		elif selection == 4:
			pass
		elif selection == 5:
			multiplier = float(input('Enter a multiplier (positive float value): '))
			original_ingredients = res['ingredients']
			new_ingredients = multiply_recipe.multiply_recipe(original_ingredients, multiplier)
			print('\nNew Original Quantities:\n', original_ingredients, '\n')
			print('New Ingredient Quantities:\n', new_ingredients, '\n')
			res['ingredients'] = new_ingredients




if __name__ == '__main__':
	if len(sys.argv) == 2:
		url = sys.argv[1]
		if url == 'default':
			url = 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'
		main(url)
	else:
		print("Invalid Number of Arguements. Run by typing 'python3 driver.py a_url'\n")
