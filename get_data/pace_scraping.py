import logging
import os

import requests
from bs4 import BeautifulSoup, Comment
from write_csv import write_csv

from get_data import constants
from get_data.parse_rows import parse_bbref_draft_row

logging. basicConfig(filename="draft.log")
logger = logging.getLogger("DRAFT_STATS")


def get_data(year):

    year_str = str(year)
    # Get all the necessary data from bbref
    # Data structure for written data. Index rows by name (and include name as one of the keys.
    all_data_dict = dict()

    # Get list of players (and nba stats)
    # Get the web page for the draft year
    draft_page = requests.get(constants.draft_url.format(year_str))
    soup = BeautifulSoup(draft_page.text, 'lxml')

    # Find the rows of data on players
    draft_table = soup.find('div', class_="table_outer_container")
    rows = draft_table.find('tbody')
    rows_list = rows.find_all('tr')
    for row in rows_list:
        try:
            if not row.find(attrs={'aria-label': "Player"}) and not row.find(attrs={'data-stat': 'header_per_g'}):
                name = row.find(attrs={'data-stat': 'player'}).text
                logger.info("getting info for {}".format(name))
                player_dict = all_data_dict.get(name, dict())
                parsed_row_dict = parse_bbref_draft_row(row)

                for key in parsed_row_dict:
                    player_dict[key] = parsed_row_dict[key]

                # Need to get blk/36 and stl/36
                #get_nba_career_data(all_data_dict[name])

                all_data_dict[name] = player_dict

        except Exception as e:
            logger.error(e)

    # Get pace-adjusted college data.


    # Write out to file

    return all_data_dict


d = get_data(2015)
write_dict_list = list()
for key in d:
    player_dict = d[key]
    player_dict['name'] = key
    write_dict_list.append(player_dict)

write_csv(write_dict_list, 'out.csv', ['NBApick_overall', 'name'])
