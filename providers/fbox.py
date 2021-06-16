import re

import lxml.html as htmlparser

from .decipher import decipher as decode

FBOX_SLUG = re.compile(r"(?:https?://)?(?:\S+\.)?fbox\.to/(?P<content_type>movie|series)/[^&?/]+-(?P<slug>[^&?/]+)")
STREAM_URL_AJAX = "https://www3.fbox.to/ajax/film/servers" 
HASH_RESOLVER_AJAX = "https://www3.fbox.to/ajax/episode/info"

MCLOUD_SLUG = re.compile(r"(?:https?://)?(?:\S+\.)?mcloud\.to/embed/(?P<slug>[^&?]+)")

def extract_from_url(url):
    if content := FBOX_SLUG.search(url):
        return content.group('content_type', 'slug')
    raise Exception('"%s" could not resolve content type and slug.' % url)

def mycloud_extraction(session, url):
    with session.get("https://mcloud.to/info/%s" % MCLOUD_SLUG.search(url).group("slug"), headers={'referer': url}) as mcloud_info:
        yield [{'quality': content.get('label', 'unknown'), 'stream_url': content.get('file', ''), 'headers': {'referer': url}} for content in mcloud_info.json().get('media', {}).get('sources', [])] 

PLAYER_RESOLVER = {
    'MyCloud': {
        'matcher': re.compile(r"(?:https?://)?(?:\S+\.)?mcloud\.to/[^&?]+"),
        'extractor': mycloud_extraction
    }
}

def get_from_player(session, player_hash):
    with session.get(HASH_RESOLVER_AJAX, params={'id': player_hash}) as response:
        real_url = decode(response.json().get('url', ''))

    for player, data in list(PLAYER_RESOLVER.items()):
        if data.get('matcher').search(real_url):
            yield from data.get('extractor', lambda s, u: [])(session, real_url)
            return

def get_movie_link(session, ajax_response_html, *, forced_check=lambda e: "MyCloud" in e.text_content()):
    """
    TODO: Remove forced check and allow user to select the stream player server.
    """
    html_element = htmlparser.fromstring(ajax_response_html) # type: htmlparser.HtmlElement
    
    for e in html_element.xpath('//li/a[@data-id]'):
        if forced_check(e):
            yield from get_from_player(session, e.get('data-id', ''))
    
def add_data(genexp, data):
    for li in genexp:
        yield [content | data for content in li]
            
def get_series_link(session, ajax_response_html, check):
    """
    TODO: Remove forced data-server selection and allow user to select the stream player server.
    """
    html_element = htmlparser.fromstring(ajax_response_html) # type: htmlparser.HtmlElement
    
    for season in html_element.xpath('//ul[@data-server="28"]'):
        for episode in season.xpath('li/a[@data-kname]'):
            if check(episode.get('data-kname')):
                yield from add_data(get_from_player(session, episode.get('data-id')), {'title': episode.get('title') or "S%sE%s" % (season.get('data-season'), episode.get('data-kname').split(':')[1])})

def fetcher(session, url, check):
    content_type, slug = extract_from_url(url)
    
    with session.get(STREAM_URL_AJAX, params={'id': slug}) as ajax_server:
        if content_type == 'movie':
            yield from add_data(get_movie_link(session, ajax_server.json().get('html', '')), {'content_type':  content_type})
        else:
            yield from add_data(get_series_link(session, ajax_server.json().get('html', ''), check), {'content_type':  content_type})
