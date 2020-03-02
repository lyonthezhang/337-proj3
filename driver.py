import sys
import web_scraping
import multiply_recipe
import parse_recipe
import cooking_method
import vegetarian
import make_italian

'''
Driver script to run recipe parsing & transformation interaction with user.
Run by typing 'python3 driver.py a_url' or 'python3 driver.py default'.
The default url is 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'
'''


def main(url):

	print('Your URL:')
	print(url, '\n')

	# Scrape recipe at user-provided url
	rf = web_scraping.RecipeFetcher()
	res = rf.scrape_recipe(url)

	# Parse and print the result from the web scraper
	print('Parsed Recipe:')
	parsed_res = parse_recipe.parse_recipe(res)
	parse_recipe.print_parsed_recipe(parsed_res)

	# ask user to select a transformation
	TRANSFORMATIONS = ['To and from vegetarian (REQUIRED)',
						'To and from healthy (REQUIRED)', 
						'Style of cuisine (AT LEAST ONE REQUIRED)', 
						'Additional Style of cuisine (OPTIONAL)', 
						'DIY to easy (OPTIONAL)', 
						'Double the amount or cut it by half (OPTIONAL)', 
						'Cooking method (OPTIONAL)']

	num_transformations = len(TRANSFORMATIONS)
	while True:
		for i in range(num_transformations):
			print(f'{i}) {TRANSFORMATIONS[i]}')
		selection = input(f'Select a transformation (integer between 0 and {num_transformations - 1}): ')
		print()

		# check that user input is a valid selection (integer between 0 & len(TRANSFORMATIONS))
		if selection in [str(x) for x in range(num_transformations)]:
			selection = int(selection)
			print(f'You selected: {TRANSFORMATIONS[selection]} \n')
		else:
			print('Invalid selection. Please try again...\n')
			continue

		# execute user-selected transformation
		if selection == 0:
			new_ingredients, new_directions = vegetarian.turn_meat_to_veggie(res)

			res['directions'] = new_directions
			res['ingredients'] = new_ingredients

			print(res['name'])
			print("\n New Directions: {} \n".format(new_directions))
			print("New Ingredients: {}".format(new_ingredients))
			print()
		
		elif selection == 1:
			pass
		
		elif selection == 2:
			new_directions, new_ingredients = make_italian.italian(res)
			res['directions'] = new_directions
			res['ingredients'] = new_ingredients


			print("New Directions: {}".format(new_directions))
			print("New Ingredients: {}".format(new_ingredients))
			print()
		
		elif selection == 3:
			pass
		
		elif selection == 4:
			pass
		
		elif selection == 5:
			multiplier = float(input('Enter a multiplier (positive float value): '))
			original_ingredients = res['ingredients']
			new_ingredients = multiply_recipe.multiply_recipe(original_ingredients, multiplier)
			print('\nOriginal Quantities:\n', original_ingredients, '\n')
			print('New Ingredient Quantities:\n', new_ingredients, '\n')
			res['ingredients'] = new_ingredients
		
		elif selection == 6:
			pass



if __name__ == '__main__':
	if len(sys.argv) == 2:
		url = sys.argv[1]
		if url == 'default':
			url = 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'
		main(url)
	else:
		print("Invalid Number of Arguements. Run by typing 'python3 driver.py a_url'\n")
