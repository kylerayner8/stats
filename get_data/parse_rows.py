
def parse_bbref_draft_row(row):
    return_data = dict()
    nba_stat_list = ['g', 'mp', 'pts', 'trb', 'ast', 'fg_pct', 'fg3_pct', 'ft_pct',
                     'mp_per_g', 'pts_per_g', 'trb_per_g', 'ast_per_g', 'ws', 'ws_per_48',
                     'bpm', 'vorp', 'pick_overall']
    try:
        player_link = row.find(attrs={'data-stat': 'player'})
        if player_link is not None:
            web_link = player_link.find('a')['href']
            return_data['bbref'] = web_link

            for stat in nba_stat_list:
                key = 'NBA' + stat
                return_data[key] = row.find(attrs={"data-stat": stat}).text

        else:
            return_data['bbref'] = None
    except Exception as e:
        raise e

    return return_data
