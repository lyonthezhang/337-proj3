from bs4 import BeautifulSoup
import requests
import re
import fractions

"""

helper functions to replace INGREDIENTS

"""

# replace vegetarian recipe with chicken as protein
def replace_veggie(meat):
    new_meat = meat.replace("(", "")
    new_meat = new_meat.replace(")", "")
    new_meat = new_meat.replace("/", " ")
    meat_lst = new_meat.split()

    original_quantity = []
    ingredient_name = ''

    # split ingredient into tokens to separate the 'quantity' from 'ingredient_name'
    for token in meat_lst:
        if any([str(digit) in token for digit in range(10)]) and not any([char in token for char in ['(', ')']]):
            fraction_obj = sum(map(fractions.Fraction, token.split()))
            as_float = int(fraction_obj)
            original_quantity.append(as_float)
        else:
            ingredient_name = ingredient_name + ' ' + token


    new_quantity = original_quantity

    if len(new_quantity) > 1:
        num = new_quantity[-1]
    else:
        num = new_quantity[0]

    replace_idx = meat_lst.index(str(num)) + 2

    replace_term = meat_lst[replace_idx: ]
    s = " "
    term = s.join(replace_term)
    veggie = meat.replace(term, "chicken")
    return veggie

# replace meat recipe with vegetarian option
def replace_meat(ingredients, meat, type_of_meat_lst, first):

    new_meat = meat.replace("(", "")
    new_meat = new_meat.replace(")", "")
    new_meat = new_meat.replace("/", " ")
    meat_lst = new_meat.split()

    original_quantity = []
    ingredient_name = ''

    # split ingredient into tokens to separate the 'quantity' from 'ingredient_name'
    for token in meat_lst:
        if any([str(digit) in token for digit in range(10)]) and not any([char in token for char in ['(', ')']]):
            fraction_obj = sum(map(fractions.Fraction, token.split()))
            as_float = int(fraction_obj)
            original_quantity.append(as_float)
        else:
            ingredient_name = ingredient_name + ' ' + token


    new_quantity = original_quantity

    if len(new_quantity) > 1:
        num = new_quantity[-1]
    else:
        num = new_quantity[0]

    replace_idx = meat_lst.index(str(num)) + 2

    # second meat replacement
    if not first:
        replace_term = meat_lst[replace_idx: ]
        s = " "
        term = s.join(replace_term)
        veggie = meat.replace(term, "veggie sausage")
        return veggie

    # ground meat replacement
    if type_of_meat_lst[0]:
        replace_term = meat_lst[replace_idx: ]
        s = " "
        term = s.join(replace_term)
        veggie = meat.replace(term, "ground tofu")
        return veggie

    # meat replacement
    if type_of_meat_lst[1]:
        replace_term = meat_lst[replace_idx: ]
        s = " "
        term = s.join(replace_term)
        veggie = meat.replace(term, "tofu")
        return veggie

    # sandwich meat replacement
    if type_of_meat_lst[2]:
        replace_term = meat_lst[replace_idx: ]
        s = " "
        term = s.join(replace_term)
        veggie = meat.replace(term, "impossible burger")
        return veggie

    # seafood replacement
    if type_of_meat_lst[3]:
        replace_term = meat_lst[replace_idx: ]
        s = " "
        term = s.join(replace_term)
        veggie = meat.replace(term, "tofuna fysh")
        return veggie

    # turkey/chicken sandwich meat replacement
    if type_of_meat_lst[4] or type_of_meat_lst[5]:
        replace_term = meat_lst[replace_idx: ]
        s = " "
        term = s.join(replace_term)
        veggie = meat.replace(term, "tofurkey")
        return veggie


"""

determine whether recipe is vegetarian or type of meat

"""
def look_for_meat(ingredients, name):
    ground_meat_lst = ['ground beef', 'ground chicken', 'ground meat', 'ground turkey', 'ground lamb', 'ground pork', 'ground bison']
    meat_lst = ['chicken', 'steak', 'beef', 'lamb', 'bacon', 'pork', 'duck', 'bison', 'rabbit', 'cow', 'sausage', 'turkey']
    sandwich_meat_lst = ['hamburger', 'cheeseburger', 'sloppy joe']
    turkey_sandwich = ['turkey', 'slice']
    chicken_sandwich = ['chicken', 'slice']
    seafood_lst = ['salmon', 'cod', 'fish', 'halibut', 'shellfish', 'crab', 'lobster', 'shrimp', 'prawn', 'scallop']
    vegetarians_lst = ['tofu', 'tofurkey', 'impossible burger', 'veggie burger']

    ground = False
    meat = False
    sandwich = False
    seafood = False
    turkey = False
    chicken = False

    vegetarian = True
    vegetarian_recipe = True

    first = True

    for n, ingredient in enumerate(ingredients):
        ingredient = ingredient.replace(".", "")
        ingredient = ingredient.replace(",", "")
        if any(x in ingredient.lower() for x in vegetarians_lst):
            new_ingredient = replace_veggie(ingredient)
            ingredients[n] = new_ingredient
            vegetarian = False
            break

        if 'bread' not in ingredient.lower():
            #if any(x in ingredient.lower() for x in turkey_sandwich):
            if 'slice' in ingredient.lower() and 'turkey' in ingredient.lower():
                turkey = True
                replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
                new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
                ingredients[n] = new_ingredient
                first = False
                vegetarian = False
                vegetarian_recipe = False
                continue
            #if any(x in ingredient.lower() for x in chicken_sandwich):
            if 'slice' in ingredient.lower() and 'chicken' in ingredient.lower():
                chicken = True
                replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
                new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
                ingredients[n] = new_ingredient
                first = False
                vegetarian = False
                vegetarian_recipe = False
                continue
        if any(x in ingredient.lower() for x in ground_meat_lst):
            ground = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            vegetarian_recipe = False
            continue
        if any(x in ingredient.lower() for x in meat_lst):
            meat = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            vegetarian_recipe = False
            continue
        if any(x in ingredient.lower() for x in sandwich_meat_lst):
            sandwich = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            vegetarian_recipe = False
            continue
        if any(x in ingredient.lower() for x in seafood_lst):
            seafood = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            vegetarian_recipe = False
            continue

    if vegetarian:
        category = get_category_recipe(name)
        if category is 'pasta':
            new_ingredient = '1 pound chicken breast'
        elif category is 'ground':
            new_ingredient = '1 pound ground beef'
        elif category is burger:
            new_ingredient = '1 pound ground beef'
        else:
            new_ingredient = '1 pound chicken breast'
        ingredients.append(new_ingredient)

    return ingredients, vegetarian_recipe

"""

change directions

"""
def change_recipe(res, change_to_meat):
    directions = res['directions']
    ingredients = res['ingredients']
    name = res['name']
    if not change_to_meat:
        new_directions = change_directions_to_meat(directions, ingredients, name)
    else:
        new_directions = change_directions_to_veggie(directions, ingredients, name)
    return new_directions

def get_category_recipe(recipe_name):
    name = recipe_name.lower()
    pasta_lst = ['pasta', 'noodle', 'mein', 'pad thai']
    main_lst = ['roasted', 'fried', 'baked']

    if any(word in name.split() for word in pasta_lst):
        return 'pasta'
    elif 'soup' in name:
        return 'soup'
    elif 'burger' in name:
        return 'burger'
    elif any(word in name.split() for word in main_lst):
        return 'main protein'
    elif 'ground' in name:
        return 'ground'
    elif 'lasagna' in name:
        return 'ground'
    elif 'rice' in name:
        return 'rice'
    return 'main protein'

def replace_veggie_direction(direction, old_word, new_word):
    words = direction.lower().split()

    idx = words.index(old_word)
    replace_this = words[idx+1]

    lower_dir = direction.lower()
    new_direction = lower_dir.replace(replace_this, new_word)

    return new_direction

# change recipe to veggie
def change_directions_to_veggie(directions, ingredients, name):
    food_category = get_category_recipe(name)

    if food_category is 'pasta':
        new_directions = get_veggie_pasta(directions, ingredients)
        return new_directions
    elif food_category is 'soup':
        new_directions = get_veggie_soup(directions, ingredients)
        return new_directions
    elif food_category is 'burger':
        new_directions = get_veggie_burger(directions, ingredients)
        return new_directions
    elif food_category is 'main protein':
        new_directions = get_veggie_main(directions, ingredients)
        return new_directions
    elif food_category is 'ground':
        new_directions = get_veggie_ground(directions, ingredients)
        return new_directions
    elif food_category is 'rice':
        new_directions = get_veggie_rice(directions, ingredients)
        return new_directions
    else:
        new_directions = get_veggie_main(directions, ingredients)
        return new_directions

# helper function to replace words in directions
def replace_direction(direction, old_word, new_word):
    direction = direction.replace(".", "")
    direction = direction.replace(",", "")
    words = direction.lower()
    new_direction = words.replace(old_word, new_word)
    return new_direction

# add new direction to make veggie burger
def get_veggie_burger(directions, ingredients):
    add_meat = True
    burger = ['pattie', 'burger', 'patti', 'hamburger', 'cheeseburger']
    new_dir = "Grill each side of veggie pattie for 5 minutes on grill."

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        words = step.lower().split()
        if any(burger) in words:
            if 'meat' in new_dir.lower().split():
                directions[n] = replace_direction(new_dir, 'meat', 'pattie')
            else:
                directions[n] = new_dir
        w = step.replace(",", "")
        if 'meat' in w:
            directions[n] = replace_direction(w.lower(), 'meat', 'pattie')

    if add_meat:
        directions.append(new_dir)

    return directions

# add new direction to make veggie pasta
def get_veggie_pasta(directions, ingredients):
    add_meat = True
    meat_lst = ['chicken', 'steak', 'beef', 'lamb', 'bacon', 'pork', 'duck', 'bison', 'rabbit', 'cow', 'sausage', 'turkey']
    new_dir = "Drizzle pan with olive oil. Stir fry chopped tofu in pan over medium heat until golden brown. Mix tofu with pasta."

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        words = step.lower().split()
        w = step.replace(",", "")
        if 'meat' in w:
            directions[n] = replace_direction(w.lower(), 'meat', 'tofu')

        #if any(meat_lst) in words:
        if any(word in words for word in meat_lst):
            directions[n] = new_dir
            add_meat = False


    if add_meat:
        directions.append(new_dir)

    return directions

# add new direction to make veggie rice
def get_veggie_rice(directions, ingredients):
    add_meat = True
    meat_lst = ['chicken', 'steak', 'beef', 'lamb', 'bacon', 'pork', 'duck', 'bison', 'rabbit', 'cow', 'sausage', 'turkey']
    new_dir = "Drizzle pan with olive oil. Stir fry chopped tofu in pan over medium heat until golden brown. Mix tofu with rice."

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        words = step.lower().split()
        if any(word in words for word in meat_lst):
            directions[n] = new_dir
            add_meat = False
        w = step.replace(",", "")
        if 'meat' in w:
            directions[n] = replace_direction(w.lower(), 'meat', 'tofu')

    if add_meat:
        directions.append(new_dir)

    return directions

# get new direction to make veggie main protein
def get_veggie_main(directions, ingredients):
    add_meat = True
    meat_lst = ['chicken', 'steak', 'beef', 'lamb', 'bacon', 'pork', 'duck', 'bison', 'rabbit', 'cow', 'sausage', 'turkey']
    new_dir = "Drizzle pan with olive oil. Stir fry chopped tofu in pan over medium heat until golden brown."

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        words = step.lower().split()
        if any(word in words for word in meat_lst):
            directions[n] = new_dir
            add_meat = False
        w = step.lower().replace(",", "")
        if 'meat' in w:
            directions[n] = replace_direction(w, 'meat', 'tofu')

    if add_meat:
        directions.append(new_dir)

    return directions

# get new direction to make ground veggie
def get_veggie_ground(directions, ingredients):
    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        words = step.lower().split()
        if 'ground' in words:
            new_dir = replace_veggie_direction(step, 'ground', 'tofu')
            d = new_dir.replace(",", "")
            if 'meat' in d.lower().split():
                directions[n] = replace_direction(new_dir, 'meat', 'ground tofu')
            else:
                directions[n] = new_dir
        if 'meat' in words:
            directions[n] = replace_direction(step, 'meat', 'ground tofu')
    return directions

# get new direction to make veggie soup
def get_veggie_soup(directions, ingredients):
    add_meat = True
    meat_lst = ['chicken', 'steak', 'beef', 'lamb', 'bacon', 'pork', 'duck', 'bison', 'rabbit', 'cow', 'sausage', 'turkey']
    new_dir = "Drizzle pan with olive oil. Stir fry chopped tofu in pan over medium heat until golden brown. Mix tofu with broth."

    for n, step in enumerate(directions):
        step = step.replace(",", "")
        step = step.replace(".", "")
        words = step.lower().split()
        if any(word in words for word in meat_lst):
            directions[n] = new_dir
            add_meat = False
        if 'meat' in step:
            step = replace_direction(step.lower(), 'meat', 'tofu')
            directions[n] = step
        if 'beef' in step:
            step = replace_direction(step.lower(), 'beef', 'tofu')
            directions[n] = step
        if 'chicken' in step:
            step = replace_direction(step.lower(), 'chicken', 'tofu')
            directions[n] = step
        if 'lamb' in step:
            step = replace_direction(step.lower(), 'lamb', 'tofu')
            directions[n] = step
        if 'sausage' in step:
            step = replace_direction(step.lower(), 'sausage', 'tofu')
            directions[n] = step
        if 'bison' in step:
            step = replace_direction(step.lower(), 'bison', 'tofu')
            directions[n] = step
        if 'steak' in step:
            step = replace_direction(step.lower(), 'steak', 'tofu')
            directions[n] = step
        if 'duck' in step:
            step = replace_direction(step.lower(), 'duck', 'tofu')
            directions[n] = step

    if add_meat:
        directions.append(new_dir)

    return directions


### meat substitutions
def change_directions_to_meat(directions, ingredients, name):
    food_category = get_category_recipe(name.lower())

    if food_category is 'pasta':
        new_directions = get_meat_pasta(directions, ingredients)
        return new_directions
    elif food_category is 'soup':
        new_directions = get_meat_soup(directions, ingredients)
        return new_directions
    elif food_category is 'burger':
        new_directions = get_meat_burger(directions, ingredients)
        return new_directions
    elif food_category is 'main protein':
        new_directions = get_meat_main(directions, ingredients)
        return new_directions
    elif food_category is 'ground':
        new_directions = get_meat_ground(directions, ingredients)
        return new_directions
    elif food_category is 'rice':
        new_directions = get_meat_rice(directions, ingredients)
        return new_directions
    else:
        new_directions = get_meat_main(directions, ingredients)
        return new_directions

# get new direction to make meat burger
def get_meat_burger(directions, ingredients):
    add_meat = True
    burger = ['impossible', 'burger']

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        if 'impossible' in step.lower().split():
            directions[n] = "Form pattie shapes with hamburger meat. Grill each side of pattie for 5 minutes at medium heat."
            add_meat = False
        elif 'veggie' in step.lower().split():
            directions[n] = "Form pattie shapes with hamburger meat. Grill each side of pattie for 5 minutes at medium heat."
            add_meat = False
        elif 'patti' in step.lower().split():
            directions[n] = "Form pattie shapes with hamburger meat. Grill each side of pattie for 5 minutes at medium heat."
            add_meat = False

    if add_meat:
        new_dir = "Form pattie shapes with hamburger meat. Grill each side of pattie for 5 minutes at medium heat."
        directions.append(new_dir)

    return directions

# get new direction to make meat pasta
def get_meat_pasta(directions, ingredients):
    add_meat = True
    burger = ['impossible', 'burger']

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        if 'tofurkey' in step.lower().split():
            directions[n] = replace_direction(step, 'tofurkey', 'chicken')
            add_meat = False
        if 'tofu' in step.lower().split():
            directions[n] = replace_direction(step, 'tofu', 'chicken')
            add_meat = False
        if 'seitan' in step.lower().split():
            directions[n] = replace_direction(step, 'seitan', 'chicken')
            add_meat = False
        if all(burger) in step.lower().split():
            directions[n] = replace_direction(step, 'burger', 'chicken')
            add_meat = False

    if add_meat:
        new_dir = "Add olive oil to a pan and chop chicken breast into bite size chunks. Then stir fry the chicken the pan at medium heat for 5 minutes each side. Mix chicken with pasta."
        directions.append(new_dir)

    return directions

# get new direction to make meat main protein
def get_meat_main(directions, ingredients):
    add_meat = True

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        if 'tofurkey' in step.lower().split():
            directions[n] = replace_direction(step, 'tofurkey', 'chicken')
            add_meat = False
        if 'tofu' in step.lower().split():
            directions[n] = replace_direction(step, 'tofu', 'chicken')
            add_meat = False
        if 'seitan' in step.lower().split():
            directions[n] = replace_direction(step, 'seitan', 'chicken')
            add_meat = False

    if add_meat:
        new_dir = "Make sure oven is at 400 degrees Farenheit. Place turkey breast on tinfoil and put in oven for 45 minutes."
        directions.append(new_dir)

    return directions

# get new direction to make meat in rice
def get_meat_rice(directions, ingredients):
    add_meat = True
    burger = ['impossible', 'burger']

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        if 'tofurkey' in step.lower().split():
            directions[n] = replace_direction(step, 'tofurkey', 'chicken')
            add_meat = False
        if 'tofu' in step.lower().split():
            directions[n] = replace_direction(step, 'tofu', 'chicken')
            add_meat = False
        if 'seitan' in step.lower().split():
            directions[n] = replace_direction(step, 'seitan', 'chicken')
            add_meat = False
        if all(burger) in step.lower().split():
            directions[n] = replace_direction(step, 'burger', 'chicken')
            add_meat = False

    if add_meat:
        new_dir = "Add olive oil to a pan and chop chicken breast into bite size chunks. Then stir fry the chicken the pan at medium heat for 5 minutes each side. Mix chicken with rice."
        directions.append(new_dir)

    return directions

# get new direction to make ground meat
def get_meat_ground(directions, ingredients):
    add_meat = True
    burger = ['impossible', 'burger']

    for n, step in enumerate(directions):
        step = step.replace(".", "")
        step = step.replace(",", "")
        if 'tofurkey' in step.lower().split():
            directions[n] = replace_direction(step, 'tofurkey', 'ground chicken')
            add_meat = False
        if 'tofu' in step.lower().split():
            directions[n] = replace_direction(step, 'tofu', 'ground chicken')
            add_meat = False
        if 'seitan' in step.lower().split():
            directions[n] = replace_direction(step, 'seitan', 'ground chicken')
            add_meat = False
        if all(burger) in step.lower().split():
            directions[n] = replace_direction(step, 'burger', 'ground chicken')
            add_meat = False

    if add_meat:
        new_dir = "Grind chicken and mix with rest of ingredients."
        directions.append(new_dir)

    return directions

# get new direction to make meat soup
def get_meat_soup(directions, ingredients):
    add_meat = True

    for n, step in enumerate(directions):
        step = step.replace(",", "")
        step = step.replace(".", "")
        if 'tofurkey' in step.lower().split():
            directions[n] = replace_direction(step, 'tofurkey', 'chicken')
            add_meat = False
        if 'tofu' in step.lower().split():
            directions[n] = replace_direction(step, 'tofu', 'chicken')
            add_meat = False
        if 'seitan' in step.lower().split():
            directions[n] = replace_direction(step, 'seitan', 'chicken')
            add_meat = False

    if add_meat:
        new_dir = "Chop chicken breast into bite size pieces. Stir fry chicken on pan with olive oil until crispy. Add to broth"
        directions.append(new_dir)

    return directions


"""
run functions
"""

def dish_has_meat(ingredients):
    meat_lst = ['hamburger', 'cheeseburger', 'corned beef', 'sloppy joe', 'chicken', \
                'steak', 'beef', 'lamb', 'bacon', 'pork', 'duck', 'bison', 'rabbit', \
                'cow', 'sausage', 'turkey', 'salmon', 'cod', 'fish', 'halibut',\
                'shellfish', 'crab', 'lobster', 'shrimp', 'prawn', 'scallop']

    for i in ingredients:
        words = i.lower().split()
        if any(word in words for word in meat_lst):
            return True

    return False

def turn_meat_to_veggie(res):
    old_ingredients = res['ingredients']
    old_directions = res['directions']
    name = res['name']

    # check if vegetarian recipe already
    veggie_recipe = dish_has_meat(old_ingredients)

    # change directions
    new_directions = change_recipe(res, veggie_recipe)

    # change ingredients
    new_ingredients, veggie_recipe = look_for_meat(old_ingredients, name)

    if not veggie_recipe:
        res['name'] = name + " - Vegetarian Version"
    else:
        if " - Vegetarian Version" in name:
            res['name'] = name.replace(" - Vegetarian Version", "")

    return new_ingredients, new_directions
