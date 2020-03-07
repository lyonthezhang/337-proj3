nut_list = ["acorn", "oak nut", "almond", "brazil nut", "candlenut", "cashew", "chestnuts", "coconut", "hazelnut", "kola nut", "macadamia", "peanut", "pecan", "pili nut", "pine nut", "pistachio", "soynuts", "walnut", "butternut", "heartnut", "assorted nuts"]
possible_nut_subs = ['soy bean','toasted kidney bean','toasted garbanzo bean','toasted split bean', 'toasted roman bean','toasted mung bean','black eyed pea','toasted pink pea','toasted black bean','toasted oat','toasted granola','crisp rice cereal','crispy chickpea','pumpkin seed','sunflower seed']

def nonut(recipe):
	directions = recipe['directions']
	ingredients = recipe['ingredients']

	print(directions, ingredients)

	cap_size = len(possible_nut_subs)
	sub_index = 0
	replacements = {}
	overflow = False
	for ingr in ingredients:
		for nut in nut_list:
			if nut in ingr and nut not in replacements.keys():
				replacements[nut] = possible_nut_subs[sub_index]
				sub_index += 1
				if sub_index == cap_size:
					sub_index = 0
					overflow = True

	i = 0
	for step in directions:
		for nut in nut_list:
			if nut in step:
				step = step.replace(nut, replacements[nut])
		if ' nut ' in step:
			if sub_index <= 9:
				step = step.replace(' nut ', ' bean ')
			elif sub_indx <= 12:
				step = step.replace(' nut ', ' beans and grains ')
			elif sub_indx > 12 or overflow == True:
				step = step.replace(' nut ', ' beans, grains, and seeds ')

		elif ' nuts ' in step:
			if sub_index <= 9:
				step = step.replace(' nuts ', ' beans ')
			elif sub_indx <= 12:
				step = step.replace(' nuts ', ' beans and grains ')
			elif sub_indx > 12 or overflow == True:
				step = step.replace(' nuts ', ' beans, grains, and seeds ')

		directions[i] = step
		i += 1

	i = 0
	for ingr in ingredients:
		for nut in nut_list:
			if nut in ingr:
				ingr = ingr.replace(nut, replacements[nut])
		if ' nut ' in ingr:
			if sub_index <= 9:
				ingr = ingr.replace(' nut ', ' bean ')
			elif sub_indx <= 12:
				ingr = ingr.replace(' nut ', ' beans and grains ')
			elif sub_indx > 12 or overflow == True:
				ingr = ingr.replace(' nut ', ' beans, grains, and seeds ')

		elif ' nuts ' in ingr:
			if sub_index <= 9:
				ingr = ingr.replace(' nuts ', ' beans ')
			elif sub_indx <= 12:
				ingr = ingr.replace(' nuts ', ' beans and grains ')
			elif sub_indx > 12 or overflow == True:
				ingr = ingr.replace(' nuts ', ' beans, grains, and seeds ')

		ingredients[i] = ingr
		i += 1

	print(directions, ingredients)
	return ingredients, directions