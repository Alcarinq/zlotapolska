import requests
from bs4 import BeautifulSoup
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

INIT_PAGE_WITH_CATEGORIES = 'https://zlotapolska.pl/medale-na-szlakach/'
PAGE_WITH_ALLVOIVODESHIPS = 'https://zlotapolska.pl'
VOIVODESHIPS_TO_BE_SKIPPED = ['Szlak Jana Pawła II', 'Złote Zamki i Pałace']
HOME_LOCATION = '49.984678658796916, 21.984831305132452'

headers = requests.utils.default_headers().update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
geolocator = Nominatim(user_agent='zlotapolska')


def read_voivodeships():
    """Read all Voivodeship """
    with requests.get(INIT_PAGE_WITH_CATEGORIES, headers=headers) as response:
        soup = BeautifulSoup(response.content, 'html.parser')
        voivodeships = soup.find_all('li', {"id": lambda l: l and l.startswith('menu-item')})
        return voivodeships


def read_places_from_single_voivodeship(voivodeship):
    """Gather all medals informations, but only for these which aren't supposed to be skipped"""
    voivodeship_name = voivodeship.find('a').getText()
    print(f"Processing started for voivodeship: {voivodeship_name}")
    if voivodeship_name not in VOIVODESHIPS_TO_BE_SKIPPED:
        voivodeship_url = PAGE_WITH_ALLVOIVODESHIPS + voivodeship.find('a').get('href')
        with requests.get(voivodeship_url, headers=headers) as response:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.find_all('article'), voivodeship_name
    else:
        return [], voivodeship_name


def read_single_medal_data(article, voivodeship_name):
    """Gather data for one medal"""
    single_medal_url = article.find('a').get('href')
    print(f"Processing: {single_medal_url}")
    with requests.get(single_medal_url, headers=headers) as art_response:
        single_article = {"name": '', 'desc': '', 'address': '', 'voivodship': ''}
        soup = BeautifulSoup(art_response.content, 'html.parser')
        single_article['name'] = soup.find('h2').getText()
        single_article['desc'] = soup.find('strong').getText() if soup.find('strong') else ''
        single_article['address'] = process_address(soup.find('div', {"class": "contact__address-taxonomy"}).find('p'))
        single_article['coordinates'] = find_coordinates(soup)
        single_article['distance'] = calculate_distance(single_article['coordinates'])
        single_article['voivodship'] = voivodeship_name
        return single_article


def process_address(address_node):
    """Process address location"""
    full_address = []
    if address_node:
        for address_part in address_node.getText().split('\n'):
            if "tel." not in address_part.lower() and \
                    ".pl" not in address_part and \
                    "tel:" not in address_part.lower() and \
                    "http" not in address_part and \
                    "www" not in address_part and \
                    "+48" not in address_part and \
                    "telefon" not in address_part and \
                    ".net" not in address_part and \
                    "087/" not in address_part and \
                    "fax" not in address_part:
                full_address.append(address_part)
        return ', '.join(full_address).strip()
    else:
        return 'BRAK'


def find_coordinates(single_article_soup):
    """Find coordinates for marker"""
    marker = single_article_soup.find('div', {'class': 'marker'})
    lat = marker.get('data-lat')
    lng = marker.get('data-lng')
    return lat, lng


def calculate_distance(coordinates):
    return f"{int(geodesic(coordinates, HOME_LOCATION).kilometers)}"
