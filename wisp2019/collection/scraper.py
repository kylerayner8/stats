import datetime
import json
import logging

import wisp2019.constants as constants
from wisp2019.collection.bbref_scraping import get_bbref_stats
from wisp2019.collection.college_scraping import get_college_stats
from wisp2019.collection.utilities import (get_data_from_draft_page_row,
                                           get_soup,
                                           get_soup_cache)

logging.basicConfig(filename="draft.log")
logger = logging.getLogger("DRAFT_STATS")


# TODO: Better exception handling.
# TODO: Better exception *messages*.
def get_nba_data_for_draft_year(year_int, write=False):
    try:
        url = constants.draft_url.format(year_int)
        soup = get_soup(url,logger)
        draft_date_tag = soup.find(lambda x: x.name == 'p' and 'Date' in x.text)
        draft_date_text = draft_date_tag.text.split(": ")[1]
        draft_datetime = datetime.datetime.strptime(draft_date_text, constants.draft_date_fmt)
        draft_table = soup.find('table', class_='stats_table').find('tbody')
        player_rows = draft_table.find_all('tr')
        # TODO: Get date of draft for age of player at draft

        for row in player_rows:
            try:
                all_stats_dict = dict()
                name = get_data_from_draft_page_row(row, 'player', logger)
                name_text = name.text
                print(name_text)
                name_url = constants.bbref_base_url + name.find('a')['href']
                
                # Get NBA data
                nba_data = get_bbref_stats(name_url, logger)

                secondary_url = nba_data.get('college_url', None)
                if secondary_url != None:
                    college_data = get_college_stats(secondary_url, logger)
                else:
                    college_data = {}
                
                all_stats_dict[name_text] = dict()
                all_stats_dict[name_text]['NBA'] = nba_data
                all_stats_dict[name_text]['NCAA'] = college_data
                all_stats_dict[name_text]['draft_date'] = draft_datetime.strftime(constants.save_fmt)
                all_stats_dict[name_text]['birth_date'] = nba_data['birth_date']

            except Exception as e:
                logger.error(e)
                continue
            
            if write:
                # TODO: Strip out special characters too?
                filename = "player_data/{}.json".format(name_text.replace(' ', ''))
                with open(filename, 'w') as f:
                    f.write(json.dumps(all_stats_dict))

    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    # TODO: Logging and data directory cleanup/setup each time this runs?
    for i in range(0, 1):
        yr = 2011 + i
        get_nba_data_for_draft_year(yr, write=True)
        print(get_soup_cache.cache_info())
