draft_url = "http://www.basketball-reference.com/draft/NBA_{0}.html"
extended_draft_url = "http://www.basketball-reference.com/play-index/draft_finder.cgi?request=1&year_min={0}&year_max={0}&college_id=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=year_id"
college_player_url = "http://www.sports-reference.com/cbb/players/{0}-{1}.html"
recruit_url = "http://www.basketball-reference.com/awards/recruit_rankings_{0}.html"

years = [2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006]

stats_header = [
    'Year',
    'Overall Pick',
    'Name',
    'RSCI',
    'Age',
    'Height',
    'Position',
    'COLLEGE',
    "SEASON",
    'ncaaG',
    'ncaaMP',
    'ncaaFG/40',
    'ncaaFGA/40',
    'ncaaFG%',
    'ncaa2P/40',
    'ncaa2PA/40',
    'ncaa2P%',
    'ncaa3P/40',
    'ncaa3PA/40',
    'ncaa3P%',
    'ncaaFT/40',
    'ncaaFTA/40',
    'ncaaFT%',
    'ncaaTRB/40',
    'ncaaAST/40',
    'ncaaSTL/40',
    'ncaaBLK/40',
    'ncaaTOV/40',
    'ncaaPF/40',
    'ncaaPTS/40',
    'NBA DIVIDER',
    'G',
    'MP',
    'PTS',
    'TRB',
    'AST',
    'FG%',
    '3P%',
    'FT%',
    'MP/G',
    'PTS/G',
    'TRB/G',
    'AST/G',
    'WS',
    'WS/48',
    'BPM',
    'VORP'
]

name_translations = {
    'Kay Felder': 'Kahlil Felder',
    'A.J. Hammons': "AJ Hammons",
    'Stephen Zimmerman': 'Stephen Zimmermanjr',
    'Larry Nance Jr.': 'Larry Nance'
}

dx_url = "http://www.draftexpress.com/stats/ncaa/2017/all/basic/per40/15/all/top100/{0}/ptspg/desc"

dx_versions = ["1", "2", "3", "4"]
