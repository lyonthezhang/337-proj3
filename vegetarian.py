from bs4 import BeautifulSoup
import requests
import re
import fractions

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

def look_for_meat(ingredients):
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

    first = True

    for n, ingredient in enumerate(ingredients):
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
                continue
            #if any(x in ingredient.lower() for x in chicken_sandwich):
            if 'slice' in ingredient.lower() and 'chicken' in ingredient.lower():
                chicken = True
                replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
                new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
                ingredients[n] = new_ingredient
                first = False
                vegetarian = False
                continue
        if any(x in ingredient.lower() for x in ground_meat_lst):
            ground = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            continue
        if any(x in ingredient.lower() for x in meat_lst):
            meat = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            continue
        if any(x in ingredient.lower() for x in sandwich_meat_lst):
            sandwich = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            continue
        if any(x in ingredient.lower() for x in seafood_lst):
            seafood = True
            replace_meat_lst = [ground, meat, sandwich, seafood, turkey, chicken]
            new_ingredient = replace_meat(ingredients, ingredient, replace_meat_lst, first)
            ingredients[n] = new_ingredient
            first = False
            vegetarian = False
            continue

    if vegetarian:
        new_ingredient = '1 pound chicken breast'
        ingredients.append(new_ingredient)

    return ingredients

    
def turn_meat_to_veggie(ingredients):
    new_ingredient = look_for_meat(ingredients)
    return new_ingredient
