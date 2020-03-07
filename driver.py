import sys
import web_scraping
import parse_recipe
import human_readable

sys.path.insert(1, './transformations')
import multiply_recipe
from healthify import healthify, unhealthify
import vegetarian
import make_italian
import lactose
import make_chinese
from get_spicy import get_spicy_recipe
import vegan
import copy
import nonut
import seafood

'''
Driver script to run recipe parsing & transformation interaction with user.
Run by typing 'python3 driver.py a_url' or 'python3 driver.py default'.
The default url is 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'
'''


def main(url):

	print()
	print(f'Your URL: {url} \n')

	# Scrape recipe at user-provided url
	rf = web_scraping.RecipeFetcher()
	res = rf.scrape_recipe(url)
	original_res = copy.deepcopy(res)

	# Parse and print the result from the web scraper
	print('***************** PARSED RECIPE FORMAT *****************')
	parsed_res = parse_recipe.parse_recipe(res)
	parse_recipe.print_parsed_recipe(parsed_res)

	print('***************** HUMAN READABLE FORMAT *****************')
	human_readable.print_ingredients(res, title='ORIGINAL INGREDIENTS')
	human_readable.print_directions(res, title='ORIGINAL DIRECTIONS')
	human_readable.print_nutrition(res, title='ORIGINAL NUTRITION')

	# ask user to select a transformation
	TRANSFORMATIONS = ['To and from vegetarian (REQUIRED)',
						'To and from healthy (REQUIRED)', 
						'To Italian (AT LEAST ONE REQUIRED)', 
						'To Chinese (OPTIONAL)', 
						'No Lactose (OPTIONAL)',
						'Double the amount or cut it by half (OPTIONAL)', 
						'More SPICYY (OPTIONAL)',
						'To vegan (OPTIONAL)',
						'Go nutless (OPTIONAL)',
						'Seafood Allergy - remove seafood (OPTIONAL)',
						'View Parsed Nutrition (OPTIONAL)',
						'Reset to Original Recipe (OPTIONAL)']

	print()
	num_transformations = len(TRANSFORMATIONS)
	while True:
		print('SELECT A TRANSFORMATION:')
		for i in range(num_transformations):
			print(f'{i}) {TRANSFORMATIONS[i]}')
		selection = input(f'Enter an integer between 0 and {num_transformations - 1}: ')
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
			if 'Vegetarian Version' in res['name']:
				human_readable.print_ingredients(res, title='VEGETARIAN INGREDIENTS')
				human_readable.print_directions(res, title='VEGETARIAN DIRECTIONS')
			else:
				human_readable.print_ingredients(res, title='NON-VEGETARIAN INGREDIENTS')
				human_readable.print_directions(res, title='NON-VEGETARIAN DIRECTIONS')	
				
		elif selection == 1:
			health_or_not = input('Would you like to go TO or FROM healthy? (TO/FROM): ')
			if health_or_not == 'TO':
				new_directions, new_ingredients = healthify(res)
				res['ingredients'] = new_ingredients
				res['directions'] = new_directions
				human_readable.print_ingredients(res, title='HEALTHY INGREDIENTS')
				human_readable.print_directions(res, title='HEALTHY DIRECTIONS')
			else:
				new_directions, new_ingredients = unhealthify(res)
				res['ingredients'] = new_ingredients
				res['directions'] = new_directions
				human_readable.print_ingredients(res, title='UNHEALTHY INGREDIENTS')
				human_readable.print_directions(res, title='UNHEALTHY DIRECTIONS')
		
		elif selection == 2:
			new_directions, new_ingredients = make_italian.italian(res)
			res['directions'] = new_directions
			res['ingredients'] = new_ingredients
			human_readable.print_ingredients(res, title='ITALIAN INGREDIENTS')
			human_readable.print_directions(res, title='ITALIAN DIRECTIONS')
		
		elif selection == 3:
			new_directions, new_ingredients = make_chinese.chinese(res)
			res['directions'] = new_directions
			res['ingredients'] = new_ingredients
			human_readable.print_ingredients(res, title='CHINESE INGREDIENTS')
			human_readable.print_directions(res, title='CHINESE DIRECTIONS')
		
		elif selection == 4:
			new_ingredients, new_directions = lactose.remove_lactose(res)
			res['ingredients'] = new_ingredients
			res['directions'] = new_directions
			human_readable.print_ingredients(res, title='NO LACTOSE INGREDIENTS')
			human_readable.print_directions(res, title='NO LACTOSE DIRECTIONS')
		
		elif selection == 5:
			multiplier = float(input('Enter a multiplier (positive float value): '))
			original_ingredients = res['ingredients']
			new_ingredients = multiply_recipe.multiply_recipe(original_ingredients, multiplier)
			res['ingredients'] = new_ingredients
			human_readable.print_ingredients(res, title='NEW INGREDIENT QUANTITIES')
		
		elif selection == 6:
			new_ingredients, new_directions = get_spicy_recipe(res)
			res['ingredients'] = new_ingredients
			res['directions'] = new_directions
			print("SPICY VERSION: {}\n".format(res['name']))
			human_readable.print_ingredients(res, title='NEW SPICY INGREDIENTS')
			human_readable.print_directions(res, title='NEW SPICY DIRECTIONS')

		elif selection == 7:
			new_ingredients, new_directions = vegan.run_vegan(res)
			res['directions'] = new_directions
			res['ingredients'] = new_ingredients
			print(res['name'])
			if 'Vegan Version' in res['name']:
				human_readable.print_ingredients(res, title='VEGAN INGREDIENTS')
				human_readable.print_directions(res, title='VEGAN DIRECTIONS')
			else:
				human_readable.print_ingredients(res, title='NON-VEGAN INGREDIENTS')
				human_readable.print_directions(res, title='NON-VEGAN DIRECTIONS')

		elif selection == 8:
			new_ingredients, new_directions = nonut.nonut(res)
			res['ingredients'] = new_ingredients
			res['directions'] = new_directions
			print("NUTLESS VERSION: {}\n".format(res['name']))
			human_readable.print_ingredients(res, title='NEW NUTLESS INGREDIENTS')
			human_readable.print_directions(res, title='NEW NUTLESS DIRECTIONS')	

		elif selection == 9:
			new_ingredients, new_directions = seafood.remove_seafood(res)
			res['ingredients'] = new_ingredients
			res['directions'] = new_directions
			human_readable.print_ingredients(res, title='NO SEAFOOD INGREDIENTS')
			human_readable.print_directions(res, title='NO SEAFOOD DIRECTIONS')

		elif selection == 10:
			# Print Nutrition
			human_readable.print_nutrition(res, title='NUTRITION')

		elif selection == 11:
			# Reset to original res
			res = copy.deepcopy(original_res)
			human_readable.print_ingredients(res, title='ORIGINAL INGREDIENTS')
			human_readable.print_directions(res, title='ORIGINAL DIRECTIONS')


if __name__ == '__main__':
	if len(sys.argv) == 2:
		url = sys.argv[1]
		if url == 'default':
			url = 'https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'
		main(url)
	else:
		print("Invalid Number of Arguements. Run by typing 'python3 driver.py a_url'\n")
