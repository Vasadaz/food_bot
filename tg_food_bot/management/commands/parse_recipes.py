from django.core.management.base import BaseCommand

import json
import logging
import time
from pathlib import Path

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

CATEGORIES = {
    'fish': 'Рыбные блюда',
    'vegetarianskoe_pitanie': 'Вегетарианские блюда',
    'bez_glutena': 'Блюда без глютена',
    'salad': 'Салаты',
    'no_diet': None,
}


def create_directory(save_dir):
    dir_path = Path(save_dir)
    Path.mkdir(dir_path, parents=True, exist_ok=True)
    return dir_path


def download_image(image_url, title, path):
    response = requests.get(image_url)
    response.raise_for_status()

    file_name = f'{title}.jpg'.replace('"', '')
    save_img_path = path / file_name
    with open(save_img_path, 'wb') as file:
        file.write(response.content)
    return save_img_path


def parse_recipes_urls(response, url):
    soup = BeautifulSoup(response, 'lxml')
    soup_of_recipes = soup.select_one('.recipe_list').select('.recipe')

    recipes_relative_urls = [recipe.select_one('a')['href'] for recipe in soup_of_recipes]
    recipes_urls = [urljoin(url, relative_url) for relative_url in recipes_relative_urls]

    return recipes_urls


def parse_recipe(response, category, image_save_path):
    soup = BeautifulSoup(response, 'lxml')
    soup_of_recipe = soup.select_one('.mcol')

    title = soup_of_recipe.select_one('.detailed').contents[0]
    description = soup_of_recipe.select_one('.detailed_full').get_text(strip=True).replace('\r\n', ' ')

    ingredients_soup = soup_of_recipe.select_one('.detailed_ingredients').select('li')
    ingredients = [' '.join(ingredient.get_text(strip=True).split()) for ingredient in ingredients_soup]

    cooking_steps_soup = soup_of_recipe.select('.detailed_step_description_big')
    cooking_steps = [step.get_text(strip=True).replace('\r\n', ' ') for step in cooking_steps_soup]

    image_url = soup_of_recipe.select_one('.bigImgBox a img')['src']
    image_path = download_image(image_url, title, image_save_path)

    recipe = {
        'title': title,
        'category': set_random_categories(category),
        'description': description,
        'ingredients': ingredients,
        'recipe': cooking_steps,
        'image': str(image_path),
    }
    return recipe


def set_random_categories(category_key: str) -> list:
    global CATEGORIES
    import random

    static_category = CATEGORIES[category_key]

    if not static_category:
        return [static_category]

    categories = list(CATEGORIES.values())
    categories.remove(None)
    random_number = random.randrange(len(categories))
    random_categories = random.sample(categories, random_number)
    if static_category not in random_categories:
        random_categories.append(CATEGORIES[category_key])

    return random_categories


def main():
    print('parsing...')
    image_save_path = create_directory('media/images')
    save_json_path = create_directory('static') / 'recipes.json'

    base_url = 'https://povar.ru/rating/{}/'
    parsing_urls = {category: base_url.format(category) for category in CATEGORIES.keys()}
    parsing_urls['no_diet'] = 'https://povar.ru/mostnew/all/'  # add recipes without filters
    recipes_urls_by_cat = {category: [] for category in CATEGORIES}
    pages_nums_to_parse = range(1, 2)
    for category, url in parsing_urls.items():
        for page in pages_nums_to_parse:
            flag = True
            while flag:
                parsing_url = f'{url}{page}'
                try:
                    response = requests.get(parsing_url)
                    response.raise_for_status()
                    recipes_urls_by_cat[category].extend(parse_recipes_urls(response.text, url))
                    break
                except requests.ConnectionError:
                    logging.info('Проблема подключения. Повторная попытка через 60 секунд.')
                    time.sleep(60)
                    continue
                except requests.HTTPError:
                    logging.info(f'Страницы {parsing_url} нет на сайте.')
                    flag = False
    recipes = {}
    for category, urls in recipes_urls_by_cat.items():
        recipes[category] = []
        for url in urls:
            flag = True
            while flag:
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    recipe = parse_recipe(response.text, category, image_save_path)
                    recipes[category].append(recipe)
                    break
                except requests.ConnectionError:
                    logging.info('Проблема подключения. Повторная попытка через 60 секунд.')
                    time.sleep(60)
                    continue
                except requests.HTTPError:
                    logging.info(f'Страницы {url} нет на сайте.')
                    flag = False
    with open(save_json_path, 'w', encoding="utf-8") as file:
        json.dump(recipes, file, indent=4, ensure_ascii=False)


class Command(BaseCommand):
    help = 'Start parse recipes'

    def handle(self, *args, **options):
        main()
