import fractions
import parse_recipe

SEAFOOD_DICT = {'salmon': 'chicken',
				'seabass': 'chicken',
				'trout': 'chicken',
				'tuna': 'chicken',
				'tilapia': 'chicken',
				'cod': 'chicken',
				'mahi mahi': 'chicken',
				'mahi': 'chicken',
				'ahi': 'chicken',
				'uni': 'chicken',
				'shark': 'chicken',
				'whale': 'chicken',
				'see urchin': 'mushroom',
				'octopus': 'mushroom',
				'sashimi': 'thin beef',
				'roe': 'peas',
				'squid': 'mushroom',
				'anchov': 'mushroom',
				'catfish': 'chicken',
				'sardine': 'chicken',
				'clam': 'mushroom',
				'scallop': 'mushroom',
				'shrimp': 'chicken',
				'prawn': 'chicken',
				'crab': 'chicken',
				'lobster': 'chicken',
				'mussel': 'mushroom',
				'oyster': 'mushroom',
				'eel': 'zuchinni',
				'crab': 'chicken',
				'fish': 'chicken'}

def remove_seafood(res):

	# replace ingredients
	new_ingredients = []
	for ingredient in res['ingredients']:
		for dairy in SEAFOOD_DICT.keys():
			if dairy in ingredient.lower() and SEAFOOD_DICT[dairy] not in ingredient.lower():
				parsed_ingredient = parse_recipe.parse_one_ingredient(ingredient)
				if dairy == 'egg':
					replacement = str(parsed_ingredient['quantity']) + ' tablespoon ' + SEAFOOD_DICT[dairy]
				else:
					replacement = str(parsed_ingredient['quantity']) + ' ' + str(parsed_ingredient['measurement']) + ' ' + SEAFOOD_DICT[dairy]
				break
			else:
				replacement = ingredient
		new_ingredients.append(replacement)

	# replace directions
	new_directions = res['directions']
	for i, step in enumerate(new_directions):
		step = step.lower()
		for sub_ing in SEAFOOD_DICT.keys():
			s = step.lower().replace(".", "")
			if sub_ing in s and SEAFOOD_DICT[sub_ing] not in s:
				new_directions[i] = new_directions[i].lower().replace(sub_ing, SEAFOOD_DICT[sub_ing])

	return new_ingredients, new_directions



