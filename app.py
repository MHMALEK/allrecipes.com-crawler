from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}


def getListOfRecepiesInCountryCuisine(countryCuisineUrl):
    response = requests.get(countryCuisineUrl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    dishesATagList = soup.find_all('a', class_='mntl-card-list-items')
    dishes = []

    for dishesATag in dishesATagList:

        dishesUrl = dishesATag.get('href')
        dish = getIngredientsForADish(dishesUrl)
        if dish:
            dishes.append(dish)

    return dishes


def getIngredientsForADish(dishUrl):
    dish = {}
    response = requests.get(dishUrl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', id='article-heading_1-0')
    if title:
        dish['title'] = title.text.strip()

    ingredients = []
    ingredientsList = soup.find_all(
        'li', class_='mntl-structured-ingredients__list-item')
    for ingredient_tag in ingredientsList:
        ingredient = {}
        quantity_tag = ingredient_tag.find(
            'span', {'data-ingredient-quantity': 'true'})
        unit_tag = ingredient_tag.find(
            'span', {'data-ingredient-unit': 'true'})
        name_tag = ingredient_tag.find(
            'span', {'data-ingredient-name': 'true'})

        if quantity_tag:
            ingredient['quantity'] = quantity_tag.text

        if unit_tag:
            ingredient['unit'] = unit_tag.text

        if name_tag:
            ingredient['name'] = name_tag.text

        ingredients.append(ingredient)

    dish['ingredients'] = ingredients
    return dish


@app.route('/get-all-dishes/<limit>', methods=['GET'])
def get_all_dishes(limit):
    url = 'https://www.allrecipes.com/cuisine-a-z-6740455'
    all_cuisines = {}
    total_count = 0
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch the webpage"}), 500

    soup = BeautifulSoup(response.content, 'html.parser')
    countryCuisineList = soup.find_all('a', class_='link-list__link')

    for countryCuisine in countryCuisineList:
        if total_count >= limit:  # Stop when reaching 200 dishes
            break
        countryCuisineName = countryCuisine.text.strip()
        countryCuisineUrl = countryCuisine.get('href')
        all_cuisines[countryCuisineName] = getListOfRecepiesInCountryCuisine(
            countryCuisineUrl)
        total_count += 1

    return jsonify(all_cuisines), 200


@app.route('/get-dishes-by-country/<country>', methods=['GET'])
def get_dishes_by_country(country):
    # You would need to adjust this logic based on how the country is represented in the URL
    country_url = f"https://www.allrecipes.com/{country}"
    dishes = getListOfRecepiesInCountryCuisine(country_url)
    return jsonify(dishes), 200


@app.route('/get-ingredients', methods=['GET'])
def get_ingredients():
    dish_url = request.args.get('url')
    if not dish_url:
        return jsonify({"error": "URL parameter is required"}), 400

    dish = getIngredientsForADish(dish_url)
    return jsonify(dish), 200


if __name__ == '__main__':
    app.run(debug=True)
