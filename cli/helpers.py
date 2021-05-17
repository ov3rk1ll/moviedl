import re

def get_check(string):
    if not string:
        return default_check
    
    return lambda s: s in ["%s:%s" % (int(_), int(e)) for _, e in re.finditer(r"(\d+):(\d+)", string)]


def check_creator(season, episode):
    return "%s:%s" % (int(season), int(episode))

default_check = lambda s: s in [*(check_creator(x, y) for y in range(100) for x in range(100))]

