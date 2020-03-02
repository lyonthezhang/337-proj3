from bs4 import BeautifulSoup
import requests

"""

define dictionary of ingredient substitutions

"""

spicy_powder = ['chili flakes', 'chili powder', 'curry powder', 'chopped habanero peppers', 'chopped jalapeno peppers']
spicy_sauce = ['sriracha', 'curry sauce', 'tabasco sauce', 'hot sauce', 'picante', 'salsa', 'wasabi']

non_spicy_spices = ['oregano', 'basil', 'thyme', 'bay leaves', 'rosemary', 'sage', \
                 'parsley',\
                    'asafoetida', 'achiote', 'allspice', 'cardamom', \
                'cayenne', 'chia seed', 'cinnamon', 'coriander', 'cumin',\
               'ginger', 'gochugaru', 'grains of paradise', 'kaffir', 'loomi', 'mace', 'mahlab',\
               'nutmeg', 'paprika', 'saffron', \
               'star anise', 'suman', 'tumeric', 'chervil', 'chive', 'cilantro',\
               'dill', 'fenugreek', 'lovage', 'marjoram', 'mint',\
                'sumemr savory','shiso', 'tarragon', 'baharat', 'bebere', 'bouquet garni', \
                'chinese five-spice powder',\
               'dukkah', 'garam masala', 'herbes de provence', 'old bay', \
                'pickling spice', 'ras el hanout',
               'sichimi togarashi', "za'atar", "taco seasoning"]
non_spicy_sauce = ['pesto', 'tomato sauce', 'guacamole', 'sour cream', 'soy sauce', 'sesame sauce', \
                   'ginger sauce', 'peanut sauce', 'yogurt sauce', 'tzatiki']



get_spicy_dict = dict.fromkeys(non_spicy_sauce[:2], 'chili flakes')
get_spicy_dict.update(dict.fromkeys(non_spicy_sauce[2:4], 'chopped jalapeno peppers'))
get_spicy_dict.update(dict.fromkeys(non_spicy_sauce[4:8], 'sriracha'))
get_spicy_dict.update(dict.fromkeys(non_spicy_sauce[8:], 'chili flakes'))
get_spicy_dict.update(dict.fromkeys(non_spicy_spices[:11], spicy_powder[0]))
get_spicy_dict.update(dict.fromkeys(non_spicy_spices[11:22], spicy_powder[1]))
get_spicy_dict.update(dict.fromkeys(non_spicy_spices[22:33], spicy_powder[2]))
get_spicy_dict.update(dict.fromkeys(non_spicy_spices[33:44], spicy_powder[3]))
get_spicy_dict.update(dict.fromkeys(non_spicy_spices[44:], spicy_powder[4]))
get_spicy_dict['taco seasoning'] = 'chili powder'
get_spicy_dict['cloves garlic'] = 'jalapeno'
get_spicy_dict['garlic powder'] = 'chili powder'
get_spicy_dict['garlic'] = 'jalapeno'




"""

helper functions

"""

def check_sauce(string):
    words = string.lower().replace(",", "").split()
    if words.count('sauce') > 1:
        idx = words.index('sauce')
        del words[idx]
        s = " "
        return s.join(words)
    else:
        return string

def get_duplicate_recipe(step, old_word, new_word):
    step = step.replace(",", "")
    step = step.replace(".", "")
    step = step.lower()
    new_str = str(old_word) + " and " + str(new_word)
    step = step.replace(old_word, new_str)
    return step


"""

run get_spicy

"""

def spicy(recipe):
    name = recipe['name']
    directions = recipe['directions']
    ingredients = recipe['ingredients']
    sub_keys = get_spicy_dict.keys()

    non_spicy_sauce = ['pesto', 'tomato sauce', 'guacamole', 'sour cream', 'soy sauce', 'sesame sauce', \
                   'ginger sauce', 'peanut sauce', 'yogurt sauce', 'tzatiki', 'taco seasoning']

    swap = False

    i = 0
    for base_ing in ingredients:
        base_ing = base_ing.lower()
        corn = 0
        for sub_ing in sub_keys:
            if sub_ing in base_ing:
                swap = True
                if any(x in sub_ing.lower() for x in non_spicy_sauce):
                    duplicate_ing = base_ing
                    ingredients.append(base_ing.replace(sub_ing, get_spicy_dict[sub_ing]))
                else:
                    ingredients[i] = ingredients[i].lower().replace(sub_ing, get_spicy_dict[sub_ing])

        # remove second 'sauce'
        if 'sauce' in ingredients[i].lower().replace(",", ""):
            ingredients[i] = check_sauce(ingredients[i])

        i += 1

    i = 0
    for step in directions:
        step = step.lower()
        for sub_ing in sub_keys:
            s = step.lower().replace(".", "")
            if sub_ing in s:
                swap = True
                if any(x in s for x in non_spicy_sauce):
                    duplicate_dir = get_duplicate_recipe(s, sub_ing, get_spicy_dict[sub_ing])
                    directions[i] = duplicate_dir
                else:
                    directions[i] = directions[i].lower().replace(sub_ing, get_spicy_dict[sub_ing])

        # remove second 'sauce'
        if 'sauce' in directions[i].lower():
            directions[i] = check_sauce(directions[i])
        i += 1

    if not swap:
        new_ing = "2 tablespoons, red chili flakes"
        new_dir = "Sprinkle red chili flakes on top of finished meal to add a little spice!"
        ingredients.append(new_ing)
        directions.append(new_dir)

    return ingredients, directions

def get_spicy_recipe(res):
    new_ingredients, new_directions = spicy(res)
    return new_ingredients, new_directions
