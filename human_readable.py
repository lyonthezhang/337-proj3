
def print_ingredients(res):
	print('----- INGREDIENTS -----')
	for i in res['ingredients']:
		print(i)
	print()

def print_directions(res):
	print('----- Directions -----')
	for index, i in enumerate(res['directions']):
		print(f'STEP {index}: {i}')
	print()