import fractions
import parse_recipe

LACTOSE_DICT = {'milk': 'soy milk [non-dairy]',
				'butter': 'i cant believe its not butter-substitute [non-dairy]',
				'parmesan': 'daiya parmesan-style shreds [non-dairy]',
				'cheddar': 'daiya cheddar-style shreds [vegan]',
				'mozzarella': 'daiya mozzarella shreds [vegan]',
				'cottage cheese': 'daiya cottage cheese-style shreds [vegan]',
				'ricotta': 'daiya ricotta-style chunks [vegan]',
				'cheese': 'daiya mozzarella shreds [vegan]',
				# 'egg white': 'mung bean egg white paste [non-dairy]',
				# 'egg': 'mung bean egg-substitute paste [non-dairy]',
				'sour cream': 'coconut milk-substitute [non-dairy]',
				'greek yogurt': 'chobani non-dairy coconut-based greek-yogurt [non-dairy]',
				'yogurt': 'forager project organic dairy-free cashewgurt [non-dairy]'}

def remove_lactose(res):

	# replace ingredients
	new_ingredients = []
	for ingredient in res['ingredients']:
		for dairy in LACTOSE_DICT.keys():
			if dairy in ingredient.lower() and LACTOSE_DICT[dairy] not in ingredient.lower():
				parsed_ingredient = parse_recipe.parse_one_ingredient(ingredient)
				if dairy == 'egg':
					replacement = str(parsed_ingredient['quantity']) + ' tablespoon ' + LACTOSE_DICT[dairy]
				else:
					replacement = str(parsed_ingredient['quantity']) + ' ' + str(parsed_ingredient['measurement']) + ' ' + LACTOSE_DICT[dairy]
				break
			else:
				replacement = ingredient
		new_ingredients.append(replacement)

	# replace directions
	new_directions = res['directions']
	for i, step in enumerate(new_directions):
		step = step.lower()
		for sub_ing in LACTOSE_DICT.keys():
			s = step.lower().replace(".", "")
			if sub_ing in s and LACTOSE_DICT[sub_ing] not in s:
				new_directions[i] = new_directions[i].lower().replace(sub_ing, LACTOSE_DICT[sub_ing])

	return new_ingredients, new_directions



