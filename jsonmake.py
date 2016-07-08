#!/usr/bin/env python3

from scrape import Scraper
import sys, json

"""
Converts the scraper output into a JSON file.
Made for Kevin Hsu's "evocheck" project, which helps people figure out which
power ranked players they might run into in bracket. If you're interested,
that's happening here: https://github.com/kevhsu/evocheck.

To run, just execute `./jsonmake.py`.
"""

if __name__ == '__main__':
    input_path = Scraper.PLAYER_FILEPATH
    output_path = sys.argv[1] if len(sys.argv) > 1 else './pools.json'
    json_content = {}
    
    with open(input_path, 'r') as ifile:
        for line in ifile:
            tag, name, pool = line.split('  &*(  ')[:3]
            pool = pool.rstrip()
            if not pool in json_content:
                json_content[pool] = {}
            json_content[pool][tag] = name
        ifile.close()

    with open(output_path, 'w') as ofile:
        json.dump(json_content, ofile, sort_keys=True, \
                indent=4, separators=(',', ': '))
        ofile.close()
