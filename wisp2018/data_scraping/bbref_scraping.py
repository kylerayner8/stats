import requests
import os
import logging
import json

import wisp2018.constants as constants

from wisp2018.data_scraping.utilities import get_soup, get_data_from_draft_page_row, get_tables_from_sportsref_page

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
        # Birthdate may be trickier to parse. 
        player_info = player_soup.find('div', id='info', class_='players')
        h = player_info.find('span', attrs={'itemprop':'height'}).text
        w = player_info.find('span', attrs={'itemprop':'weight'}).text
        rc_rank = player_info.find(lambda a: a.name == 'p' and "Recruiting" in a.text)
        try:
            l = rc_rank.text.replace(' ', '').replace('\n', '').strip('RecruitingRank:').split(u'\xa0')
        except:
            logger.error("No recruit rank for {}".format(url))
            l = "N/A"
        all_nba_data['height'] = h
        all_nba_data['weight'] = w
        all_nba_data['recruit_rank'] = l

        
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
