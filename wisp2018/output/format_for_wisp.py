import json
import logging
import os

from wisp2018.output.csv_writer import write_csv

headers = ['Name','Year','RSCI','Age','Height','Pos','College',
'ncaaG','ncaaMP','ncaaFGA','ncaa2PM','ncaa2PA','ncaa2PER','ncaa3PM',
'ncaa3PA','ncaa3PER','ncaaFTM','ncaaFTA','ncaaFTPER','ncaaORB',
'ncaaDRB','ncaaTRB','ncaaAST','ncaaSTL','ncaaBLK','ncaaTOV',
'ncaaPF','BPM1','BPM2','BPM3','BPM4','BPM5']


def parse_player_for_writing(player_stats_dict, logger):
    try:
        d_out = dict()
        pname = list(player_stats_dict.keys())[0]
        stats = player_stats_dict[pname]
        
        d_out['Name'] = pname
        c_stats = stats['NCAA']
        if len(c_stats.keys()) < 1:
            return {}
        n_stats = stats['NBA']
        # find last college year
        years = list(c_stats['players_per_game'].keys())
        yparsed = list()
        for y in years:
            yparsed.append(y.strip('players_per_game.'))
        d_out['Year'] = sorted(yparsed)[-1]
        d_out['RSCI'] = n_stats['recruit_rank'][1].strip('(').strip(')')
        # TODO: make me not cry when I get this age. 
        first_nba_age = float(n_stats['per_game'][sorted(list(n_stats['per_game'].keys()))[0]]['age'])
        print(first_nba_age)
        d_out['Age'] = first_nba_age - 1
        d_out['Height'] = n_stats['height']
        # TODO: need to add position to scraping
        d_out['Pos'] = 'soon'
        cystats = c_stats['players_per_poss']['players_per_poss.{}'.format(d_out['Year'])]
        d_out['College'] = cystats['school_name']
        d_out['ncaaG'] = cystats['g']
        d_out['ncaaMP'] = cystats['mp']
        
        # Pace adjusted stats
        pace = float(c_stats['players_per_game']['players_per_game.{}'.format(d_out['Year'])]['ps_per_g'])
        statfactor = 72.0/pace
        d_out['ncaaFGA'] = float(cystats['fga_per_poss']) * statfactor
        d_out['ncaa2PM'] = float(cystats['fg2_per_poss']) * statfactor
        d_out['ncaa2PA'] = float(cystats['fg2a_per_poss']) * statfactor
        d_out['ncaa2PER'] = float(cystats['fg2_pct'])
        d_out['ncaa3PM'] = float(cystats['fg3_per_poss']) * statfactor
        d_out['ncaa3PA'] = float(cystats['fg3a_per_poss']) * statfactor
        d_out['ncaa3PER'] = float(cystats['fg3_pct']) if cystats['fg3_pct'] != "" else 0
        d_out['ncaaFTM'] = float(cystats['ft_per_poss']) * statfactor
        d_out['ncaaFTA'] = float(cystats['fta_per_poss']) * statfactor
        d_out['ncaaFTPER'] = float(cystats['ft_pct'])
        # TODO: sports ref doesn't split these out in pace stats
        # d_out['ncaaORB'] = cystats['']
        # d_out['ncaaDRB']
        d_out['ncaaTRB'] = float(cystats['trb_per_poss']) * statfactor
        d_out['ncaaAST'] = float(cystats['ast_per_poss']) * statfactor
        d_out['ncaaSTL'] = float(cystats['stl_per_poss']) * statfactor
        d_out['ncaaBLK'] = float(cystats['blk_per_poss']) * statfactor
        d_out['ncaaTOV'] = float(cystats['tov_per_poss']) * statfactor
        d_out['ncaaPF'] = float(cystats['pf_per_poss']) * statfactor

        # NBA stats
        # d_out['BPM1']
        # d_out['BPM2']
        # d_out['BPM3']
        # d_out['BPM4']
        # d_out['BPM5']
        k = 1
        for key in sorted(n_stats['advanced'].keys()):
            if k > 5:
                break
            bpm = n_stats['advanced'][key]['bpm']
            d_out['BPM{}'.format(k)] = bpm
            k+=1
        
        index = 1
        for key in sorted(n_stats['per_poss'].keys()):
            if index > 5:
                break
            d_out['nbaG{}'.format(index)] = n_stats['per_poss'][key]['g']
            d_out['nbaMP{}'.format(index)] = n_stats['per_poss'][key]['mp']
            d_out['nbaFG{}'.format(index)] = n_stats['per_poss'][key]['fg_per_poss']
            d_out['nbaFGA{}'.format(index)] = n_stats['per_poss'][key]['fga_per_poss']
            d_out['nbaFGPER{}'.format(index)] = n_stats['per_poss'][key]['fg_pct']
            d_out['nba3PM{}'.format(index)] = n_stats['per_poss'][key]['fg3_per_poss']
            d_out['nba3PA{}'.format(index)] = n_stats['per_poss'][key]['fg3a_per_poss']
            d_out['nba3PER{}'.format(index)] = n_stats['per_poss'][key]['fg3_pct']
            d_out['nba2PM{}'.format(index)] = n_stats['per_poss'][key]['fg2_per_poss']
            d_out['nba2PA{}'.format(index)] = n_stats['per_poss'][key]['fg2a_per_poss']
            d_out['nba2PER{}'.format(index)] = n_stats['per_poss'][key]['fg2_pct']
            d_out['nbaFT{}'.format(index)] = n_stats['per_poss'][key]['ft_per_poss']
            d_out['nbaFTA{}'.format(index)] = n_stats['per_poss'][key]['fta_per_poss']
            d_out['nbaFTPER{}'.format(index)] = n_stats['per_poss'][key]['ft_pct']
            d_out['nbaORB{}'.format(index)] = n_stats['per_poss'][key]['orb_per_poss']
            d_out['nbaDRB{}'.format(index)] = n_stats['per_poss'][key]['drb_per_poss']
            d_out['nbaTRB{}'.format(index)] = n_stats['per_poss'][key]['trb_per_poss']
            d_out['nbaAST{}'.format(index)] = n_stats['per_poss'][key]['ast_per_poss']
            d_out['nbaSTL{}'.format(index)] = n_stats['per_poss'][key]['stl_per_poss']
            d_out['nbaBLK{}'.format(index)] = n_stats['per_poss'][key]['blk_per_poss']
            d_out['nbaTOV{}'.format(index)] = n_stats['per_poss'][key]['tov_per_poss']
            d_out['nbaPF{}'.format(index)] = n_stats['per_poss'][key]['pf_per_poss']
            
            index += 1
        
        return d_out
    
    except Exception as e:
        logger.error(pname)
        logger.error(e, exc_info=True)
        return {}


def write_stats(stats_dict_list, logger):
    try:
        write_csv(stats_dict_list, 'out.csv', headers)
    except Exception as e:
        logger.error(e, exc_info=True)


def test_parser():
    
    logging.basicConfig(filename="write.log")
    logger = logging.getLogger("WISP_WRITE")
    stats_d_list = list()
    # TODO: make this location dynamic
    for filename in os.listdir('/Users/ian/wisp/player_data'):
        with open('/Users/ian/wisp/player_data/'+filename) as f:
            d = json.loads(f.read())
        d = parse_player_for_writing(d, logger)
        stats_d_list.append(d)
    write_stats(stats_d_list, logger)

if __name__ == '__main__':
    test_parser()