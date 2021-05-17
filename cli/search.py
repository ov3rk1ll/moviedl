"""
Search results resolver.
"""

import lxml.html as htmlparser

SEARCH_AJAX = "https://swatchseries.ru/ajax/film/search"
BASE = "https://swatchseries.ru"

def search(session, query):
    
    with session.get(SEARCH_AJAX, params={'keyword': query}) as ajax_search_results:
        html_element = htmlparser.fromstring(ajax_search_results.json().get('html'))
        
    for search_results in html_element.xpath('//a[@class="item"]'):
        yield {'name': search_results.xpath('div[@class="info"]/div[@class="title"]')[0].text_content(), 'url': BASE + search_results.get('href')}