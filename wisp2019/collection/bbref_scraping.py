import datetime
import logging

from wisp2019.collection.utilities import get_soup, get_tables_from_sportsref_page

logging. basicConfig(filename="draft.log")
logger = logging.getLogger("DRAFT_STATS")


def get_bbref_stats(url, logger):
    
    try:
        player_soup = get_soup(url, logger)

        # Get all data from this page
        all_nba_data = get_tables_from_sportsref_page(player_soup, logger)
        
        # TODO: Get measureables.
        # Maybe also get from college page? Need to check that out.
        # Height, weight, position, recruit rank (if available). 
        # Birth date may be trickier to parse.
        player_info = player_soup.find('div', id='info', class_='players')
        player_height = player_info.find('span', attrs={'itemprop':'height'}).text
        player_weight = player_info.find('span', attrs={'itemprop':'weight'}).text
        rc_rank = player_info.find(lambda a: a.name == 'p' and "Recruiting" in a.text)
        birth_date = player_info.find('span', id="necro-birth").attrs["data-birth"]
        try:
            player_rank = rc_rank.text.replace(' ', '').replace('\n', '').strip('RecruitingRank:').split(u'\xa0')[0]
            player_rank = player_rank.split('(')[1]
            player_rank = player_rank.strip(')')
        except Exception as e:
            logger.error("No recruit rank for {}: {}".format(url, e))
            player_rank = "N/A"
        all_nba_data['height'] = player_height
        all_nba_data['weight'] = player_weight
        all_nba_data['recruit_rank'] = player_rank
        all_nba_data['birth_date'] = birth_date

        
        # Get secondary stats url
        # TODO: this can be from "Euro Stats at Basketball-Reference.com" for players
        # like Porzingis. Need to handle that case as well.
        try:
            college_stats_url = player_soup.find(text="College Basketball at Sports-Reference.com").parent['href']
        except:
            logger.error("No college stats link for {}".format(url))
            college_stats_url = None
        all_nba_data['college_url'] = college_stats_url
        
        return all_nba_data

    except Exception as e:
        logger.error("Error getting stats from {}: {}".format(url, e), exc_info=True)
        return {}
