import re
from typing import List
import requests
from bs4 import BeautifulSoup as bs
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