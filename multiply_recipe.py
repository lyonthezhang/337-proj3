import fractions

MEASUREMENT_WORDS = ['cup', 'oz', 'ounce', 'pound', 'clove', 'teaspoon', 'tsp', 'tablespoon', 'tbs', 'egg', 'jar', 'package', 'pack', 'can']

def multiply_recipe(ingredients_list, multiplier):
    
    new_ingredients_list = []
    
    # go through each ingredient in the recipe
    for ingredient in ingredients_list:
        tokens = ingredient.split()
        original_quantity = 0
        ingredient_name = ''
        
        # split ingredient into tokens to separate the 'quantity' from 'ingredient_name'
        for token in tokens:            
            if any([str(digit) in token for digit in range(10)]) and not any([char in token for char in ['(', ')']]):
                fraction_obj = sum(map(fractions.Fraction, token.split()))
                as_float = float(fraction_obj)
                original_quantity += as_float
            else:
                ingredient_name = ingredient_name + ' ' + token

        # multiply amount by 'multiplier'
        new_quantity = original_quantity * multiplier
        
        # check if 'new_quantity' crosses 1
        # append/delete plural 's' from end of measurement word
        # Ex: 3 cups --> 1 cup, 1/2 tablespoon --> 2 tablespoons
        if original_quantity <= 1 and new_quantity > 1:
            tokens = ingredient_name.split()
            if tokens[0] in MEASUREMENT_WORDS:
                tokens[0] = ' '+ tokens[0] + 's'
            ingredient_name = ' '.join(tokens)
        elif original_quantity > 1 and new_quantity <= 1:
            tokens = ingredient_name.split()
            if tokens[0][0:-1] in MEASUREMENT_WORDS:
                tokens[0] = tokens[0][0:-1]
            ingredient_name = ' ' + ' '.join(tokens)
        
        # convert float to mixed fraction
        base = int(new_quantity // 1)
        if base == new_quantity:
            new_num = str(base) + ' '
        elif new_quantity < 1:
            frac = fractions.Fraction.from_float(new_quantity).limit_denominator()
            new_num = str(frac)
        else:
            frac = fractions.Fraction.from_float(new_quantity % base).limit_denominator()
            new_num = str(base) + ' ' + str(frac)
        
        # update the multiplied quantity in the ingredients list
        if new_quantity != 0:
            new_ingredients_list.append(new_num + ingredient_name)
        else:
            new_ingredients_list.append(ingredient_name[1:])
          
    return new_ingredients_list