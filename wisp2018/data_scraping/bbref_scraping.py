import requests
import os
import logging
import json

import wisp2018.constants as constants

from wisp2018.data_scraping.utilities import get_soup, get_data_from_draft_page_row, get_tables_from_sportsref_page
from wisp2018.data_scraping.utilities import test_json

logging. basicConfig(filename="draft.log")
logger = logging.getLogger("DRAFT_STATS")

# TODO: Better exception handling.
# TODO: Better exception *messages*.
def get_nba_data_for_draft_year(year_int):
    try:
        url = constants.draft_url.format(year_int)
        soup = get_soup(url,logger)
        draft_table = soup.find('table', class_='stats_table').find('tbody')
        player_rows = draft_table.find_all('tr')
        # player_rows = [player_rows[0]]

        for row in player_rows:
            try:
                all_stats_dict = dict()
                name = get_data_from_draft_page_row(row, 'player', logger)
                name_text = name.text
                print(name_text)
                name_url = constants.bbref_base_url + name.find('a')['href']

                player_soup = get_soup(name_url, logger)

                # TODO: Get measureables.
                # Maybe also get from college page? Need to check that out. 

                # Get all data from this page
                all_nba_stats = get_tables_from_sportsref_page(player_soup, logger)

                # Get data from college
                # TODO: this can be from "Euro Stats at Basketball-Reference.com" for players
                # like Porzingis. Need to handle that case as well. 
                college_stats_url = player_soup.find(text="College Basketball at Sports-Reference.com").parent['href']
                college_soup = get_soup(college_stats_url, logger)
                all_college_stats = get_tables_from_sportsref_page(college_soup, logger)

                all_stats_dict[name_text] = dict()
                all_stats_dict[name_text]['NBA'] = all_nba_stats
                all_stats_dict[name_text]['NCAA'] = all_college_stats

            except Exception as e:
                logger.error(e)
                continue
            
            # TODO: Strip out special characters too?
            filename = "player_data/{}.json".format(name_text.replace(' ', ''))
            with open(filename, 'w') as f:
                f.write(json.dumps(all_stats_dict))

    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    # TODO: Logging and data directory cleanup/setupeach time this runs?
    get_nba_data_for_draft_year(2015)