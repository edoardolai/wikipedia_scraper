import requests
from bs4 import BeautifulSoup as bs
import json
from typing import Dict
from get_first_paragraph import get_first_paragraph
from multiprocessing import Pool

def get_leaders()->Dict:
    '''Extract leaders information from provided data and calls internally get_first_paragraph() to extract relevant paragraph about leader's life.'''
    #REGEXES
    # These two regexes for removing pronunciation characters (usually found between / /)
    phonetics_regex = r"/.*?/" 
    valid_characters_regex = r"[^\w\s.,;:!?()«»'’\u00C0-\u017F-]+" 
    # Remove foot-note references e.g [1]
    sq_brackets_regex = r"\[.*?\]"  
    #Remove non breaking spaces characters
    nbsp_regex = r"\xa0"  
    #Remove non meaninful words left after removing pronounciation characters
    french_pronunciation_regex = r"[;:]*\s?\(?\s?È?Écouter\s?\)?"

    regexes = [phonetics_regex, sq_brackets_regex,nbsp_regex, valid_characters_regex,french_pronunciation_regex]

    #initialize urls
    root_url = "https://country-leaders.onrender.com"
    cookie_url = f"{root_url}/cookie"
    countries_url = f"{root_url}/countries"
    
    #initialize sessions
    on_render_session = requests.Session()
    wiki_session = requests.Session()
    cookies = requests.get(cookie_url).cookies
    on_render_session.cookies = cookies

    #fetch country
    countries = on_render_session.get(countries_url).json()
    leaders_per_country = {}

    #fetch leader data
    for country in countries:
        try:
            leaders = list()
            leaders_data = on_render_session.get(f"{root_url}/leaders?country={country}")
            # Set new cookies if they expired
            if leaders_data.status_code != 200 and leaders_data.json().get("message") == "The cookie is expired":
                new_cookies = requests.get(cookie_url).cookies
                on_render_session.cookies = new_cookies
                leaders = on_render_session.get(f"{root_url}/leaders?country={country}").json()
            else:
                leaders = leaders_data.json()
        except Exception as e:
            print(f"Something went wrong: {e}")

        leaders_urls = [(leader["wikipedia_url"], leader["id"], regexes, wiki_session) for leader in leaders_data.json()]
        with Pool() as pool:
            res = pool.starmap(get_first_paragraph, leaders_urls)
            for leaders_idx, leader in enumerate(leaders):
                leader["bio"] = res[leaders_idx]
            leaders_per_country[country] = leaders
    return leaders_per_country

def save(leaders_per_country: Dict, file_name: str, indent: int = 4):
    '''Saves leaders dictionary to .json file with specified file name. Indent parameter allows indentation customisazion (default: 4)'''
    with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(leaders_per_country, file, ensure_ascii=False, indent=indent)

if __name__ == '__main__':
    leaders_dict = get_leaders()
    save(leaders_dict,'leaders')