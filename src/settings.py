import os
from dotenv import load_dotenv
load_dotenv()

ENDPOINT_SET = "recipes/complexSearch"
SESSION_HEADERS_SET = {"Application": "spoonacular",
                           "Content-Type": "application/x-www-form-urlencoded"}
API_ROOT_SET = "https://api.spoonacular.com/"
API_KEY_SET = os.getenv('api_key_env')
DB_NAME_SET = 'db.sqlite3'
DB_TABLE_NAME_SET = 'requested_meals'