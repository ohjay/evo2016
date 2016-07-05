#!/usr/bin/env python3

from scrape import Scraper
import datetime
import calendar
import sys

"""
Processes player data and turns it into a minimalist HTML page.
Assumes that the scraper script has already been run.
"""

class Parser(object):
    TOP_100_PATH = './top100.txt'
    DEFAULT_CONTENT = '<!DOCTYPE html><html><head><meta charset=utf-8><meta name="description"' \
        + ' content="A compiled, updatable list of EVO 2016 Super Smash Bros. Melee entrants."/>' \
        + '<title>EVO 2016 Player List</title><link href=assets/stylesheets/normalize.min.css ' \
        + 'rel=stylesheet><link href=assets/stylesheets/style.css rel=stylesheet><script ' \
        + 'src="assets/javascripts/script.js"></script></head><body><h1>EVO 2016 ' \
        + 'Player List</h1><h2>Last updated on %s</h2>%s<h3>Sleeper Picks [MIOM > 100] ' \
        + '(<a id="toggle-link" href="#" onclick="toggleSleepers();return false;">Show</a>)' \
        + '</h3><div id="sleeper" style="display: none">%s</div></body></html>'
    
    HEADER = '<div class="table-row-item">%s</div>'
    DATA = '<div class="table-row-item" data-header="%s">%s</div>'
    ROW_HEADER = '<div class="table-header table-row">%s</div>'
    ROW_DATA = '<div class="table-row">%s</div>'
    TABLE = '<div class="table">%s%s</div>'
    POOL_LINK = '<a href="%s" target="_blank">Pool %s</a>'
    
    DROPOUTS = ('Kevin Nanney') # :(
    CONFIRMED = {'Jeffrey Williamson': ('Axe', 'E611')} # :)
    
    def __init__(self, html_path='./index.html', content=None):
        self.html_path = html_path
        self.content = content if content is not None else Parser.DEFAULT_CONTENT
        self.players, self.names = [], []
        self.load_players()
        
        now = datetime.datetime.now()
        month = calendar.month_name[now.month]
        ordinal = self.get_ordinal(now.day)
        
        self.date = '%s %d%s' % (month, now.day, ordinal)
        
    def load_players(self):
        with open(Scraper.PLAYER_FILEPATH, 'r') as pfile:
            for line in pfile:
                tokens = line.split('  &*(  ')
                self.players.append(tokens)
                self.names.append(tokens[1].lower())
            pfile.close()
    
    def write(self):
        miom100_tables, sleeper_tables = '', ''
        
        # Fill in the top 100 MIOM players, if they're attending
        rank, count_idx = 1, 0
        header_grp, data_grp = '', ''
        with open(Parser.TOP_100_PATH, 'r') as tfile:
            for top100_name in tfile:
                top100_name = top100_name.rstrip()
                if len(top100_name) < 3:
                    continue
                try:
                    if top100_name in Parser.CONFIRMED:
                        # The player is ONLY in Parser.CONFIRMED
                        tag, pool = Parser.CONFIRMED[top100_name]
                    else:
                        name_idx = self.names.index(top100_name.lower())
                        if top100_name in Parser.DROPOUTS:
                            rank += 1
                            del self.players[name_idx]
                            del self.names[name_idx]
                            continue
                    
                        tag, name, pool = self.players.pop(name_idx)
                        del self.names[name_idx]
                    
                        pool = pool.rstrip()
                    
                    header_grp += Parser.HEADER % (tag + ' (#' + str(rank) + ')')
                    data_grp += self.make_data(tag, pool, rank)
                    count_idx = (count_idx + 1) % 4
                    
                    if count_idx == 0:
                        miom100_tables += self.make_table(header_grp, data_grp)
                        header_grp = ''
                        data_grp = ''
                except ValueError as e:
                    pass # not necessarily bad
                rank += 1
            
            while count_idx != 0:
                header_grp += Parser.HEADER % ''
                data_grp += Parser.DATA % ('', '')
                count_idx = (count_idx + 1) % 4
            if header_grp:
                miom100_tables += self.make_table(header_grp, data_grp)
            tfile.close()
        
        header_grp, data_grp = '', ''
        count_idx = 0
        for tag, name, pool in self.players:
            pool = pool.rstrip()
            header_grp += Parser.HEADER % tag
            data_grp += self.make_data(tag, pool)
            count_idx += 1
            
            if count_idx == 4:
                tbl = self.make_table(header_grp, data_grp)
                sleeper_tables += tbl.replace('"table"', '"table sleeper-top"')
                header_grp, data_grp = '', ''
            elif count_idx % 4 == 0:
                sleeper_tables += self.make_table(header_grp, data_grp)
                header_grp, data_grp = '', ''
        
        while count_idx % 4 != 0:
            header_grp += Parser.HEADER % ''
            data_grp += Parser.DATA % ('', '')
            count_idx += 1
        if header_grp:
            sleeper_tables += self.make_table(header_grp, data_grp)
        
        hfile = open(self.html_path, 'w')
        hfile.write(self.content % (self.date, miom100_tables, sleeper_tables))
        hfile.close()
    
    def make_data(self, tag, pool, rank=None):
        header_txt = tag + (' (#' + str(rank) + ')' if rank else '')
        pool_url = Scraper.POOL_URL % pool.lower()
        pool_link = Parser.POOL_LINK % (pool_url, pool)
        
        return Parser.DATA % (header_txt, pool_link)
    
    def make_table(self, header_grp, data_grp):
        hrow = Parser.ROW_HEADER % header_grp
        drow = Parser.ROW_DATA % data_grp
        
        return Parser.TABLE % (hrow, drow)
    
    def get_ordinal(self, day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            return 'th'
        else:
            return ['st', 'nd', 'rd'][day % 10 - 1]
        
if __name__ == '__main__':
    html_path = sys.argv[1] if len(sys.argv) > 1 else './index.html'
    parser = Parser(html_path=html_path)
    parser.write()
