from bs4 import BeautifulSoup
import requests

from bs4 import BeautifulSoup
import requests
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}
url = 'https://www.allrecipes.com/cuisine-a-z-6740455'


def getListOfRecepiesInCountryCuisine(countryCuisineUrl):
    response = requests.get(countryCuisineUrl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    dishesATagList = soup.find_all('a', class_='mntl-card-list-items')

    for dishesATag in dishesATagList:
        dishesUrl = dishesATag.get('href')
        getIngredientsForADish(dishesUrl)


def getIngredientsForADish(dishUrl):
    dish = {}
    response = requests.get(dishUrl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', id='article-heading_1-0').text
    dish['title'] = title.strip()

    ingridientsList = soup.find_all(
        'li', class_='mntl-structured-ingredients__list-item')
    for ingridient in ingridientsList:
       # Extract data
        quantity = ingridient.find(
            'span', {'data-ingredient-quantity': 'true'}).text
        unit = ingridient.find('span', {'data-ingredient-unit': 'true'}).text
        name = ingridient.find('span', {'data-ingredient-name': 'true'}).text

        # Create an object (dictionary)
        ingredient = {
            'quantity': quantity,
            'unit': unit,
            'name': name
        }
        dish['ingredient'] = ingredient
        print(dish)
        return ingredient


response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Failed to fetch the webpage")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
countryCuisineATagList = soup.find_all('a', class_='link-list__link')

for countryCuisineATag in countryCuisineATagList:
    countryCuisineUrl = countryCuisineATag.get('href')
    getListOfRecepiesInCountryCuisine(countryCuisineUrl)
