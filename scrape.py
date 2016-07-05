#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse

"""
A scraper for gathering user-specified data about EVO 2016.
Primary purpose: to accumulate and format an SSBM attendee list.
"""

class Scraper(object):
    POOL_URL = 'http://evo2016.s3.amazonaws.com/brackets/ssbm_%s.html'
    PLAYER_FILEPATH = './players.txt'
    POOLS = []
    
    def __init__(self):
        if not Scraper.POOLS:
            self.initialize_pools()
    
    def initialize_pools(self):
        """Because let's be honest – I don't want to type it all in myself."""
        for prefix in ('a', 'b', 'c', 'd', 'e'):
            for i in range(601, 626):
                Scraper.POOLS.append(prefix + str(i))
        for i in range(601, 625):
            Scraper.POOLS.append('f%s' % str(i))
    
    def scrape(self, label):
        if label.lower().startswith('p'):
            print('[o] Scraping EVO 2016 players. Please wait...')
            f = open(Scraper.PLAYER_FILEPATH, 'w')
            for pool in Scraper.POOLS:
                self.scrape_pool(pool, f)
            f.close()
            print('[+] Finished!')
        else:
            print('[-] Label not recognized.')
        
    def scrape_pool(self, pool, f):
        print('[o] Scraping pool %s...' % pool.upper())
        page = requests.get(Scraper.POOL_URL % pool)
        soup = BeautifulSoup(page.content, 'lxml')
        
        player_handles = soup.find_all('div', {'class': 'player-handle'})
        player_names = soup.find_all('div', {'class': 'player-name'})
        
        for i in range(min(len(player_handles), len(player_names))):
            handle = ''.join(player_handles[i].find_all(text=True)) \
                    .replace('&nbsp;', '').replace(' ', '')
            name = ''.join(player_names[i].find_all(text=True)) \
                    .replace('&nbsp;', '').replace(' ', '')
            
            if not handle:
                if len(name) > 0 and not name.lower().startswith('bye'):
                    f.write('%s  &*(  %s  &*(  %s\n' % (name, \
                            name, pool.upper()))
                continue
            f.write('%s  &*(  %s  &*(  %s\n' % (handle, name, pool.upper()))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('label', help='desired information')
    args = parser.parse_args()
    
    scraper = Scraper()
    scraper.scrape(args.label)
