import inspect
import json
import sqlite3
import requests
from database_manager import DatabaseManager
from enum import Enum
from settings import *
from typing import List

class RequestMethodEnum(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'

class RecipesClient:
    def __init__(self):
        self.db = DatabaseManager(DB_NAME_SET, DB_TABLE_NAME_SET)
        try:
            self.db.get_records()
        except sqlite3.OperationalError:
            self.db.init_database()

    def search_recipes_complex_search(self, include_ingredients: List, exclude_ingredients: List, fill_ingredients=True,
                                      limit_license=None, number='5', add_recipe_information=True,
                                      add_recipe_nutrition=True,
                                      sort='min-missing-ingredients'):
        """ Find recipes that use as many of the given ingredients
            as possible and have as little as possible missing
            ingredients. This is a whats in your fridge API endpoint.
            https://spoonacular.com/food-api/docs#search-recipes-by-ingredients
        """
        endpoint = ENDPOINT_SET
        url_params = {"fillIngredients": fill_ingredients, "includeIngredients": include_ingredients,
                      'excludeIngredients': exclude_ingredients, "limitLicense": limit_license,
                      'sort': sort, "number": number, "addRecipeInformation": add_recipe_information,
                      'addRecipeNutrition': add_recipe_nutrition}
        return self.make_request(endpoint, method=RequestMethodEnum.GET.value, params=url_params)

    def make_request(self, path, method=RequestMethodEnum.GET.value, endpoint=None, query={}, params={}, json=None):
        """ Make a request to the API """
        session = requests.Session()
        session.headers = {
            "Application": "spoonacular",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        api_root = API_ROOT_SET
        api_key = API_KEY_SET
        timeout = 5
        sleep_time = 1.5
        sleep_time = max(sleep_time, 1)
        # Check if the API call cost will exceed the quota
        endpoint = inspect.stack()[1].function
        uri = api_root + path

        # API auth (temporary kludge)
        if params:
            params['apiKey'] = api_key
        else:
            params = {'apiKey': api_key}
        response = session.request(method, uri,
                                   timeout=timeout,
                                   data=query,
                                   params=params,
                                   json=json)
        self.db.insert_record(self.give_hash_key(params['includeIngredients'], params['excludeIngredients']),
                              self.get_meals_info(response))

        return response

    @staticmethod
    def remove_comma(ingredient):
        ingredient.replace(',', '')
        return ingredient

    @staticmethod
    def remove_space(ingredient):
        ingredient.replace(' ', '')
        return ingredient

    def give_hash_key(self, used_ingr: str, missed_ingr: str):
        used_ingr = self.remove_comma(used_ingr)
        used_ingr = self.remove_space(used_ingr)
        missed_ingr = self.remove_comma(missed_ingr)
        missed_ingr = self.remove_space(missed_ingr)

        return used_ingr + 'exclude' + missed_ingr

    def get_meals_info(self, request):
        matching_meals = {}
        request_info = request.json()['results']

        for elem in request_info:
            matching_meals[elem['title']] = {'image': elem['image'],
                                             'usedIngredients': self.get_used_miss_ingredients(elem['usedIngredients']),
                                             'missedIngredients': self.get_used_miss_ingredients(elem['missedIngredients'], missed=True),
                                             'calories': elem['nutrition']['nutrients'][0]['amount'],
                                             'carbs': elem['nutrition']['nutrients'][3]['amount'],
                                             'proteins': elem['nutrition']['nutrients'][8]['amount']
                                             }
        matching_meals['Best Meal Option'] = self.get_best_meal(matching_meals)
        return matching_meals

    @staticmethod
    def sort_meals_by_nutrition(meals_nutrition_values):
        sorted_meals = sorted(sorted(meals_nutrition_values, key=lambda x: x[1]), key=lambda x: x[0], reverse=True)

        return sorted_meals

    @staticmethod
    def get_first_element_sorted_best_meals(meals_with_nutrition, sorted_meals_with_nutrition):
        return list(meals_with_nutrition.keys())[list(meals_with_nutrition.values()).index(sorted_meals_with_nutrition[0])]

    def get_best_meal(self, matching_meals):
        meals_with_nutrition = {}
        for key in matching_meals:
            meals_with_nutrition[key] = [matching_meals[key]['proteins'], matching_meals[key]['carbs']]
        sorted_meals_with_nutrition = self.sort_meals_by_nutrition(meals_with_nutrition.values())
        return self.get_first_element_sorted_best_meals(meals_with_nutrition, sorted_meals_with_nutrition)

    def make_request_or_get_db(self, hash_key: str, include_ingr, exclude_ingr):
        data = self.db.get_record(hash_key)
        if not data:
            data = self.get_meals_info(
                self.search_recipes_complex_search(include_ingredients=include_ingr, exclude_ingredients=exclude_ingr))
        else:
            data = self.parse_json_str_to_dict(data[0])
        return data

    @staticmethod
    def parse_json_str_to_dict(data):
        data = data.replace("'", '"')
        return json.loads(data)

    def get_used_miss_ingredients(self, used_ingredients, missed=False):
        list_of_ingredients = []
        for elem in used_ingredients:
            if missed:
                ingredient = elem['name']
                list_of_ingredients.append(ingredient)
            else:
                ingredient = elem['name']
                list_of_ingredients.append(ingredient)
        return list_of_ingredients
