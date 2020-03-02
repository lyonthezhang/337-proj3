
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