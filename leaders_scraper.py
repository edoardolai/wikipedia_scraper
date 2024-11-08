import re
import requests
from bs4 import BeautifulSoup as bs
import json
from typing import List,Dict

def get_first_paragraph(wikipedia_url: str, regexes:List[str], session: requests.Session) -> str:
    '''Returns relevant paragraph from provided url page.'''
    first_paragraph = ''
    leader_data = bs(session.get(wikipedia_url).content, 'html.parser')
    paragraphs = leader_data.find_all("p")
    
    for par in paragraphs:
        if par.find('b') is not None:
            first_paragraph = par.get_text()
            break
    
    for regex in regexes:
        first_paragraph = re.sub(regex, '', first_paragraph)
    
    return first_paragraph.strip()


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
        for leader in leaders:
            leader["bio"] = get_first_paragraph(leader["wikipedia_url"], regexes,wiki_session)
        leaders_per_country[country] = leaders
    return leaders_per_country

def save(leaders_per_country: Dict, file_name: str, indent: int = 4):
    '''Saves leaders dictionary to .json file with specified file name. Indent parameter allows indentation customisazion (default: 4)'''
    with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(leaders_per_country, file, ensure_ascii=False, indent=indent)

leaders_dict = get_leaders()

save(leaders_dict,'leaders')