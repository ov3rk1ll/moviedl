import argparse
from providers import get_appropriate

import requests

from cli.helpers import *
from cli.search import search
from cli.download import cli_download

def __movie_dl__():
    
    session = requests.Session()
    
    parser = argparse.ArgumentParser(description="movie-dl is a high quality movie/series download and/or grabber.")
    
    parser.add_argument('-s', '--search', required=False, default='', help="Query for searching from WatchSeries.")
    parser.add_argument('--iafl', action="store_true", help="'I am feeling lucky' mode, that is, the first result (if search is used) will be enqueued for download.")
    
    parser.add_argument('-dl', '--download', required=False, default='', help="Download from a valid url.")
    parser.add_argument('-l', '--list', required=False, default='', help="Selections of episode (if series).")
    parser.add_argument('-o', '--output-folder', required=False, default='', help="Folder to which the content would be downloaded.")
    
    parser.add_argument('-g', '--grab', required=False, default='', help="Grab the stream link(s) without downloading.")
    parser.add_argument('-q', '--quiet', action="store_true", help="Quiet mode, basically for disabling tqdm.")
    
    parsed = parser.parse_args()
    dl_check = get_check(parsed.list)
    
    if parsed.search:
        print("Searching for '%s' on WatchSeries:" % parsed.search)
        
        results = [*search(session, parsed.search)]
        
        if not results:
            print("Could not find anything from that identifier.")
        
        for index, content in enumerate(results, 1):
            print("{0:02d}: {name} \x1b[33m{url}\x1b[0m".format(index, **content))
            
        if not parsed.iafl:
            return
        
        if not results:
            return print("'I am feeling lucky' cannot continue since there are no results.")
        
        first_result = results.pop(0)
        url = first_result.get('url')
        
        for qualities in get_appropriate(session, url, check=dl_check):            
            cli_download(session, qualities, first_result.get('name'), parsed.quiet)
            
    if parsed.download:
        for qualities in get_appropriate(session, parsed.download, check=dl_check):            
            cli_download(session, qualities, parsed.output_folder or 'Downloads', parsed.quiet)
                
    if parsed.grab:
        for qualities in get_appropriate(session, parsed.grab, check=dl_check):            
            print(', '.join(q.get('stream_url') for q in qualities))
            print("Headers for above stream(s): %s" % ', '.join("%s" % q.get('headers', {}) for q in qualities))

if __name__ == '__main__':
    __movie_dl__()