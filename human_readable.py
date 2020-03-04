
def print_ingredients(res, title='INGREDIENTS'):
	print(f'------ {title} ------')
	for i in res['ingredients']:
		print(i)
	print()

def print_directions(res, title='DIRECTIONS'):
	print(f'------ {title} ------')
	for index, i in enumerate(res['directions']):
		print(f'STEP {index}: {i}')
	print()

def print_nutrition(res, title='NUTRITION'):
	print(f'-------- {title} --------')
	data = []
	n_servings = res['calories_and_servings'][0]
	n_calories = res['calories_and_servings'][2]
	data.append(['Servings', str(n_servings), ''])
	data.append(['Calories', str(n_calories), ''])

	for key in res['nutrition']:
		amt = res['nutrition'][key][0]
		percent = res['nutrition'][key][1]
		data.append([key, amt, percent])
		# print(f"{key}: {amt} {percent}")
	col_width = max(len(word) for row in data for word in row) + 2  # padding
	# col_width = 20
	for row in data:
	    print("".join(word.ljust(col_width) for word in row))
	print()