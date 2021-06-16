import re

def get_check(string):
    if not string:
        return default_check
    
    def check(s):
        season, episode = s.split(":")
        blocks = string.split(" ")
        for b in blocks:
            _s, _e = b.split(":")
            # season must match, episode can be the actual value or X
            if season == _s and (_e == "X" or episode == _e):
                return True

        return False

    return check


def check_creator(season, episode):
    return "%s:%s" % (int(season), int(episode))

default_check = lambda s: s in [*(check_creator(x, y) for y in range(100) for x in range(100))]

