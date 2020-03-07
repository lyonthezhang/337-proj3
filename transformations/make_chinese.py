from bs4 import BeautifulSoup

"""

define meats, herbs, and sauces dictionary

"""
non_chinese_herbs = ['asafoetida', 'achiote', 'allspice', 'cardamom', 'cayenne',\
                'gochugaru', 'grains of paradise', 'kaffir', 'loomi', 'mace', 'mahlab',\
                'nutmeg', 'paprika', 'saffron', 'suman', 'tumeric', 'chervil',\
                'dill', 'fenugreek', 'lovage', 'marjoram', 'mint',\
                'oregano', 'thyme', 'bay leaves', 'rosemary', 'sage', \
                'parsley', 'chili powder', 'chili flakes', 'garlic',\
                'sumemr savory','shiso', 'tarragon', 'baharat', 'bebere', 'bouquet garni', \
                'chili powder', 'dukkah', 'garam masala', 'herbes de provence', 'old bay', \
                'pickling spice', 'ras el hanout', 'shichimi togarashi', "za'atar", "taco seasoning"]

non_chinese_fish = ['salmon', 'tuna','sardine','herring','tilapia','catfish','trout','mackerel','anchovy','perch','pike']
non_chinese_sauces = ['ginger','salsa','guacamole','picante','tomato','alfredo','mushroom','steak','barbecue','marinara','mayonnaise','tartar','garlic']
non_chinese_lipids = ['butter','olive oil','coconut oil','avocado oil','canola oil','vegetable oil']
non_chinese_peppers = ['jalapeno','habanero','chipotle']
non_chinese_noodles = ['spaghetti noodle','fettuccine noodle','fettuccini noodle','capellini noodle','angel hair noodle','tagliatelle noodle','linguine noodle']
non_chinese_grains = ['penne','orzo','farfelle','macaroni','rotini','rigatoni','gnocchi']
non_chinese_vinegar = ['balsamic vinegar','red wine vinegar','sherry vinegar','apple cider vinegar']

# create dictionary
chinese_dict = dict.fromkeys(non_chinese_sauces[:4], 'soy sauce')
chinese_dict.update(dict.fromkeys(non_chinese_fish[4:8], 'hoison sauce'))
chinese_dict.update(dict.fromkeys(non_chinese_fish[8:], 'sweet and sour sauce'))
chinese_dict['browning sauce'] = 'soy sauce'
chinese_dict['pinto beans'] = 'soybeans'
chinese_dict['black beans'] = 'soybeans'
chinese_dict['refried beans'] = 'soybeans'
chinese_dict['chive'] = 'chinese chive'
chinese_dict['basil'] = 'thai basil'
chinese_dict['bison'] = 'beef'
chinese_dict.update(dict.fromkeys(non_chinese_vinegar[:], 'rice vinegar'))
chinese_dict.update(dict.fromkeys(non_chinese_grains[:], 'white rice'))
chinese_dict.update(dict.fromkeys(non_chinese_noodles[:], 'wheat noodle'))
chinese_dict.update(dict.fromkeys(non_chinese_peppers[:], 'chili'))
chinese_dict.update(dict.fromkeys(non_chinese_lipids[:], 'sesame oil'))
chinese_dict.update(dict.fromkeys(non_chinese_fish[:4], 'sea bass'))
chinese_dict.update(dict.fromkeys(non_chinese_fish[4:8], 'cod'))
chinese_dict.update(dict.fromkeys(non_chinese_fish[8:], 'haddock'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[:5], 'coriander'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[5:10], 'thai basil'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[10:15], 'lemongrass'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[15:20], 'star anise'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[20:25], 'fenugreek'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[25:30], 'galangal'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[30:35], 'cloves'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[35:40], 'turmeric'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[40:45], 'five-spice'))
chinese_dict.update(dict.fromkeys(non_chinese_herbs[45:], 'cumin'))

"""

helper functions for making recipe chinese

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

make recipe chinese

"""

def chinese(recipe):
    directions = recipe['directions']
    ingredients = recipe['ingredients']
    sub_keys = chinese_dict.keys()

    i = 0
    for base_ing in ingredients:
        base_ing = base_ing.lower()
        corn = 0
        for sub_ing in sub_keys:
            if sub_ing in base_ing:
                if sub_ing is 'beef':
                    corn = check_corn_beef(base_ing)
                if corn == 1:
                    ingredients[i] = ingredients[i].replace('corn beef', chinese_dict[sub_ing])
                    break
                if corn == 2:
                    ingredients[i] = ingredients[i].replace('corned beef', chinese_dict[sub_ing])
                    break
                else:
                    ingredients[i] = ingredients[i].lower().replace(sub_ing, chinese_dict[sub_ing])

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
                directions[i] = directions[i].lower().replace(sub_ing, chinese_dict[sub_ing])

        # remove second 'sauce'
        if 'sauce' in directions[i].lower():
            directions[i] = check_sauce(directions[i])
        i += 1

    return directions, ingredients
