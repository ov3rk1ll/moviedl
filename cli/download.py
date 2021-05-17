from tqdm import tqdm
from pathlib import Path

def filter_content(content, *, ext='mp4'):
    for q in content:
        if q.get('stream_url').endwith(ext):
            return q 

def download(session, url, headers, size, path_to_file, *, use_tqdm, bar):
    d = 0
    with open(path_to_file, 'ab') as sw:
        d = sw.tell()
        if use_tqdm:
            bar.update(d)
            
        while size > d:
            for chunks in session.get(url, stream=True, headers={'Range': 'bytes=%d-' % d} | headers or {},).iter_content(0x4000):
                sz = len(chunks)
                d += sz
                if use_tqdm:
                    bar.update(sz)
                sw.write(chunks)


def cli_download(session, content, identifier, quiet_mode):
    
    downloadable = filter_content(content)
    
    if not downloadable:
        print("Failed to download one of %s's content due to the lack of a valid 'mp4' download link.\n\n" \
            "Full content fetch was: %s" % (identifier, content))
        return
    
    with session.head(downloadable.get('stream_url'), headers=downloadable.get('headers') or {}) as head_response:
        content_length = int(head_response.headers.get('content-length') or 0)
    
    Path('./{slug}'.format(slug=identifier)).mkdir(exist_ok=True)
    
    t = None
    if not quiet_mode:
        t = tqdm(desc='Downloading %s.mp4' % downloadable.get('title', 'movie'), unit_scale=True, unit='B', total=content_length)
    
    return download(session, downloadable.get('stream_url'), downloadable.get('headers') or {}), content_length, Path("./{slug}/%s.mp4").format(slug=identifier, en=downloadable.get('title', 'movie'), use_tqdm=(not quiet_mode), bar=t)
