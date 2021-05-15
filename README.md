# Meals recomendation

## Description
- Program uses Spoonacular Api and from given avaible products and products you don't want to have in your meal returns best max 5 meals to prepare (min missing ingredients). 
- After first request with specified ingredients data is stored in database so, if later you choose same arguments there will be no request and data will be taken from data base.
- Output is generated html file created with Jinja2 which is stored in recipies directory
- In output you will get informations like: best meals with used and missing ingredients, amount of proteins and carbs and also meal picture.
- You will also get best meal option which is choosen by minimum carbs and maximum amount of proteins. 

## Install

- Create a virtual environment using virtualenv venv
- Activate the virtual environment by running source venv/bin/activate
- On Windows use source venv\Scripts\activate
- Install the dependencies using pip install -r requirements.txt
- Run program by using: cd src and after that: python food_search.py

Generated recipes are stored in recipes directory
