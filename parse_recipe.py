import fractions

##### CONSTANTS #####
VESSEL = ['pot', 'pan', 'skillet', 'baking sheet', 'bowl', 'cutting board']
TOOLS = ['mixer', 'blender', 'food processor']
UTENSILS = ['knife', 'fork', 'spoon', 'whisk', 'spatula', 'brush']
ALL_TOOLS = VESSEL + TOOLS + UTENSILS

MEASUREMENT_WORDS = ['cup', 'oz', 'ounce', 'pound', 'clove', 'teaspoon', 'tsp', 'tablespoon', 'tbs', 'jar', 'package', 'pack', 'can', 'bottle', 'pinch', 'pinches']
PLURAL_MEASUREMENT_WORDS = [x + 's' for x in MEASUREMENT_WORDS]
ALL_MEASUREMENT_WORDS = MEASUREMENT_WORDS + PLURAL_MEASUREMENT_WORDS

COOKING_METHODS = ['boil', 'bake', 'broil', 'saute', 'brown', 'toast', 'stir fry', 'pan fry', 'deep fry', 'sear', 'braise', 'poach', 'beat', 'mix', 'blend', 'whisk', 'fold']

TIME_WORDS = ['second', 'minute', 'hour'] #'sec', 'min', 'hr'


def parse_ingredients(ingredients_list):

    parsed_ingredients = []

    for ingredient in ingredients_list:
        tokens = ingredient.split()
        quantity = 0
        name = ''
        measurement = ''

        # assign token to 'quantity', 'measurement', or 'name'
        for token in tokens:
            if any([str(digit) in token for digit in range(10)]) and not any([char in token for char in ['(', ')']]):
                fraction_obj = sum(map(fractions.Fraction, token.split()))
                as_float = float(fraction_obj)
                quantity += as_float
            elif any([token in x for x in ALL_MEASUREMENT_WORDS]) or any([char in token for char in ['(', ')']]):
                measurement += token + ' '
            else:
                name = name + token + ' '
        parsed_ingredients.append({'name': name[0:-1],
                                   'quantity': quantity,
                                   'measurement': measurement[0:-1]})

    return parsed_ingredients

def parse_tools(directions_list):
    tools = []
    for tool in ALL_TOOLS:
        if any([tool in step.lower() for step in directions_list]):
            tools.append(tool)
    return tools

def parse_methods(directions_list):
    methods = []
    for method in COOKING_METHODS:
        if any([method in step.lower() for step in directions_list]):
            methods.append(method)
    return methods

def parse_steps(directions_list, ingredients, tools, methods):
    parsed_steps = []
    ingredients = [x['name'] for x in ingredients]
    for step in directions_list:
        step_dict = {}
        step_dict['text'] = step
        step_dict['ingredients'] = [x for x in ingredients if any([(i in x.lower() and len(i) > 2) for i in step.split()])]
        step_dict['tools'] = parse_tools([step]) if parse_tools([step]) != [] else None
        step_dict['methods'] = parse_methods([step]) if parse_methods([step]) != [] else None
        step_dict['time'] = get_time(step) if get_time(step) != [] else None
        
        parsed_steps.append(step_dict)
    return parsed_steps

def get_time(step):
    times = []
    for x in TIME_WORDS:
        if x in step:
            splits = step.split(x)
            for i in range(len(splits) - 1):
                before = step.split(x)[i]
                number = before.split()[-1]
                times.append(number + ' ' + x)
    return times
    
def parse_recipe(res):
    
    parsed_recipe = {}
    parsed_recipe['ingredients'] = parse_ingredients(res['ingredients'])
    parsed_recipe['tools'] = parse_tools(res['directions'])
    parsed_recipe['methods'] = parse_methods(res['directions'])
    parsed_recipe['steps'] = parse_steps(res['directions'], parsed_recipe['ingredients'], parsed_recipe['tools'], parsed_recipe['methods'])
    
    return parsed_recipe

def print_parsed_recipe(parsed_res):
    print("Ingredients")
    for x in parsed_res['ingredients']:
        print(x)

    print()
    print(f"Methods \n{parsed_res['methods']}")

    print()
    print(f"Tools \n{parsed_res['tools']}")

    print()
    print('Steps')
    for i, step in enumerate(parsed_res['steps']):
        ingredients = ', '.join(step['ingredients']) if step['ingredients'] else None
        methods = ', '.join(step['methods']) if step['methods'] else None
        tools = ', '.join(step['tools']) if step['tools'] else None
        time = ', '.join(step['time']) if step['time'] else None
        print(f"{i}) Text: {step['text']}")
        print(f"   Ingredients: {ingredients}; Methods: {methods}; Tools: {tools}; Time: {time}")
        # print(f"   Methods: {step['methods']}")
        # print(f"   Tools: {step['tools']}")
        # print(f"   Time: {step['time']}")
        print()
