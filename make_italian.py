from bs4 import BeautifulSoup
import requests

"""

define meats, herbs, and sauces dictionary

"""

italian_herbs = ['oregano', 'basil', 'thyme', 'bay leaves', 'rosemary', 'sage', \
                 'parsley', 'chili powder', 'chili flakes', 'garlic']
italian_meats = ['chicken', 'proscuitto', 'meatball']
italian_sauces = ['tomato sauce', 'italian red sauce', 'pesto']

non_italian_herbs = ['asafoetida', 'achiote', 'allspice', 'cardamom', \
                'cayenne', 'chia seed', 'cinnamon', 'coriander', 'cumin',\
               'ginger', 'gochugaru', 'grains of paradise', 'kaffir', 'loomi', 'mace', 'mahlab',\
               'nutmeg', 'paprika', 'saffron', \
               'star anise', 'suman', 'tumeric', 'chervil', 'chive', 'cilantro',\
               'curry', 'dill', 'fenugreek', 'lovage', 'marjoram', 'mint',\
                'sumemr savory','shiso', 'tarragon', 'baharat', 'bebere', 'bouquet garni', \
                'chili powder', 'chinese five-spice powder',\
               'dukkah', 'garam masala', 'herbes de provence', 'old bay', \
                'pickling spice', 'ras el hanout',
               'sichimi togarashi', "za'atar", "taco seasoning"]
non_italian_meats = ['beef', 'salmon', 'cod', 'tuna', 'crab', 'clam', 'mussel', 'scallop', 'shrimp', 'tofu', 'seitan',\
                    'duck', 'sausage', 'rib', 'lamb', 'steak', 'bison']
non_italian_sauces = ['soy', 'sesame', 'ginger', 'peanut', 'hot sauce', 'salsa', 'guacamole', 'picante']

# create dictionary
italian_dict = dict.fromkeys(non_italian_sauces, 'tomato sauce')
italian_dict['brisket'] = 'meat'
italian_dict['browning sauce'] = 'tomato sauce'
italian_dict['cheddar'] = 'mozzarella'
italian_dict['pinto beans'] = 'garbanzo beans'
italian_dict['black beans'] = 'garbanzo beans'
italian_dict['fried beans'] = 'garbanzo beans'
italian_dict.update(dict.fromkeys(non_italian_meats[:6], 'chicken'))
italian_dict.update(dict.fromkeys(non_italian_meats[6:], 'beef'))
italian_dict.update(dict.fromkeys(non_italian_herbs[:5], 'oregano'))
italian_dict.update(dict.fromkeys(non_italian_herbs[5:10], 'basil'))
italian_dict.update(dict.fromkeys(non_italian_herbs[10:15], 'thyme'))
italian_dict.update(dict.fromkeys(non_italian_herbs[15:20], 'bay leaves'))
italian_dict.update(dict.fromkeys(non_italian_herbs[20:25], 'rosemary'))
italian_dict.update(dict.fromkeys(non_italian_herbs[25:30], 'sage'))
italian_dict.update(dict.fromkeys(non_italian_herbs[30:35], 'oregano'))
italian_dict.update(dict.fromkeys(non_italian_herbs[35:40], 'garlic powder'))
italian_dict.update(dict.fromkeys(non_italian_herbs[40:45], 'rosemary'))
italian_dict.update(dict.fromkeys(non_italian_herbs[45:], 'thyme'))

"""

helper functions for making recipe italian

"""
def check_corn_beef(string):
    words = string.lower().split()
    idx = words.index('beef')
    if words[idx - 1] == 'corn':
        return 1
    if words[idx - 1] == 'corned':
        return 2
    else:
        return 0

def check_sauce(string):
    words = string.lower().replace(",", "").split()
    if words.count('sauce') > 1:
        idx = words.index('sauce')
        del words[idx]
        s = " "
        return s.join(words)
    else:
        return string


"""

make recipe italian

"""

def italian(recipe):
    directions = recipe['directions']
    ingredients = recipe['ingredients']
    sub_keys = italian_dict.keys()

    i = 0
    for base_ing in ingredients:
        base_ing = base_ing.lower()
        corn = 0
        for sub_ing in sub_keys:
            if sub_ing in base_ing:
                if sub_ing is 'beef':
                    corn = check_corn_beef(base_ing)
                    print(base_ing)
                    print(corn)
                if corn == 1:
                    ingredients[i] = ingredients[i].replace('corn beef', italian_dict[sub_ing])
                    break
                if corn == 2:
                    ingredients[i] = ingredients[i].replace('corned beef', italian_dict[sub_ing])
                    break
                else:
                    ingredients[i] = ingredients[i].lower().replace(sub_ing, italian_dict[sub_ing])

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
                directions[i] = directions[i].lower().replace(sub_ing, italian_dict[sub_ing])

        # remove second 'sauce'
        if 'sauce' in directions[i].lower():
            directions[i] = check_sauce(directions[i])
        i += 1

    return directions, recipe
