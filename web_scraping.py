from bs4 import BeautifulSoup
import requests
import re


def get_numbers(lst):
    new_list = [int(x.split(':')[1]) if ':' in x else -1 for x in lst]
    return new_list


class RecipeFetcher:

    search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'

    def search_recipes(self, keywords):
        search_url = self.search_base_url %(keywords.replace(' ','+'))

        page_html = requests.get(search_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")

        return [recipe.a['href'] for recipe in page_graph.find_all('div', {'class':'grid-card-image-container'})]

    def scrape_recipe(self, recipe_url):
        results = {}

        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")

        find_name = [name.text for name in\
                          page_graph.find_all('h1', {'id': 'recipe-main-content'}, {'class': 'recipe-summary__h1'})]
        results['name'] = find_name[0]

        results['ingredients'] = [ingredient.text for ingredient in page_graph.find_all('span', {'itemprop':'recipeIngredient'})]

        results['directions'] = [direction.text.strip() for direction in page_graph.find_all('span', {'class':'recipe-directions__list--item'}) if direction.text.strip()]

        results['nutrition'] = self.scrape_nutrition_facts(recipe_url)

        results['calories_and_servings'] = self.scrape_calories_servings(recipe_url)

        return results

    def scrape_nutrition_facts(self, recipe_url):
        results = []

        nutrition_facts_url = '%s/fullrecipenutrition' %(recipe_url)

        page_html = requests.get(nutrition_facts_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")

        r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")

        nutrient = {}

        for nutrient_row in page_graph.find_all('div', {'class': 'nutrition-row'}):

            lst = nutrient_row.text.split(':')
            amount_lst = lst[1]
            name = lst[0].replace('\n', '')

            amount = amount_lst.split('\n')
            amount = [x.replace(' ', '') for x in amount[:2]]

            nutrient[name] = amount

        return nutrient

    def scrape_calories_servings(self, recipe_url):
        """
        returns [servings per recipe, amt per serving, calories]
        """

        nutrition_facts_url = '%s/fullrecipenutrition' %(recipe_url)

        page_html = requests.get(nutrition_facts_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")

        r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")

        nutrient = {}

        for row in page_graph.find_all('div', {'class': 'nutrition-top light-underline'}):
            lst = row.text.split('\n')
            lst = list(filter(lambda a: a != '\r', lst))

            calories = [x.lstrip() for x in lst]
            calories.pop()
            info = get_numbers(calories)

            return info
