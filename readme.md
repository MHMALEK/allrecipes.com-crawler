# My Web Scraper API

This project is a web scraping tool that collects data from allrecipes.com and provides it through a Flask-based RESTful API. Users can request information on dishes, including ingredients and other details.

## Endpoints

- `GET /get-all-dishes`: Returns JSON data containing up to 200 dishes from all country cuisines.
- `GET /get-dishes-by-country/{country}`: Returns JSON data containing the dishes for a specific country cuisine.
- `GET /get-ingredients?url={dish_url}`: Returns JSON data containing the ingredients for the specified dish.

## Installation

### Requirements

- Python 3.6 or higher
- Flask
- BeautifulSoup

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```

2. Navigate to the project directory:

```bash
cd your-repo-name
```

3. Install dependencies:

```bash
    pip install -r requirements.txt
```

```bash
python app.py
```

The server will start, and the API will be accessible at http://localhost:5000.

# Deployment

in progress...

# License

This project is licensed under the MIT License - see the LICENSE.md file for details.

# Disclaimer

Only for personal and non-commercial use. All rights and content belongs to www.allrecipes.com and I don't use their data on my own.
