import logging
import os

import requests
from bs4 import BeautifulSoup, Comment

from get_data import constants

logging. basicConfig(filename="draft.log")
logger = logging.getLogger("DRAFT_STATS")

#TODO: Get scout consensus
#TODO: lots of cleanup.


def format_nba_data(player_row):
    name = player_row.find(attrs={'data-stat': 'player'}).text
    return name, player_row


def format_player_name_for_sports_ref(player_name):
    """
    Takes a player's full name and formats it for use in a 
    sports-reference url. 
    """
    formatted_name = player_name.replace(" III", "")
    formatted_name = formatted_name.replace(".", "")
    formatted_name = formatted_name.replace("'", "")
    formatted_name = formatted_name.replace(" ", "-")
    formatted_name = formatted_name.lower()
    name_split = formatted_name.split(" ")

    return formatted_name


def get_college_data(player_name, year_str, player_index):
    try:
        if player_name in constants.name_translations.keys():
            name = constants.name_translations[player_name]
        else:
            name = player_name
        first_last = name.split(" ")
        url_name = format_player_name_for_sports_ref(name)
        url = constants.college_player_url.format(url_name, player_index)
        page = requests.get(url)
        if page.status_code == 404:
            logger.warning("no data available for: {}".format(player_name))
            return None, None, None

        college_soup = BeautifulSoup(page.text, 'lxml')
        height = ""
        position = ""
        try:
            height = college_soup.find('span', attrs={'itemprop': 'height'}).text
            position = college_soup.find_all('strong')[1].parent.contents[2]
        except Exception as e:
            pass
        position_formatted = position.strip()

        # Get the /40 stats table from the page
        tables = college_soup.find_all(text=lambda text: text and isinstance(text, Comment) and 'Per 40 Minutes Table' in text)
        table_soup = BeautifulSoup(tables[0], 'lxml')
        stat_rows = table_soup.find('tbody').find_all('tr')
        # Check if this player is old enough to not have /40 stats.
        if stat_rows == None:
            logger.warning("No per 40 stats, trying {0} ({1}) {2}".format(player_name, url_name, player_index+1))
            return get_college_data(player_name, year_str, player_index + 1)

        # Check if this is the wrong player with this name.
        recent_season = stat_rows[-1]
        if year_str[-2:] != recent_season.find(attrs={"data-stat": "season"}).text[-2:]:
            logger.warning("BAD YEAR, TRYING {0} ({1}) {2}".format(player_name, url_name, player_index+1))
            return get_college_data(player_name, year_str, player_index+1)

        return_dict = {
            'recent_season': recent_season,
            'height': height,
            'position_formatted': position_formatted
        }
        return return_dict

    except Exception as e:
        logger.error("Something went wrong with: {0}:{1}".format(player_name, e))
        return None


def format_for_csv(nba_row, college_row, player_age, player_height, player_position, player_combined_dict, year):
    name = nba_row.find(attrs={'data-stat': 'player'}).text
    data_row_list = list()

    # Add identifying info
    data_row_list.append(year)
    # Format: data_row_list.append(nba_row.find(attrs={"data-stat": ""}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "pick_overall"}).text)
    data_row_list.append(name)
    # Placeholder for RSCI
    data_row_list.append("")
    data_row_list.append(player_age)
    data_row_list.append(player_combined_dict['height'])
    #data_row_list.append(player_height)
    data_row_list.append(player_position)
    # Not necessary right now
    #data_row_list.append(nba_row.find(attrs={"data-stat": "college_name"}).text)
    #data_row_list.append(nba_row.find(attrs={"data-stat": "team_id"}).text)

    # Add college stats
    # Might be None, so need to account for that
    data_row_list.append(nba_row.find(attrs={"data-stat": "college_name"}).text.replace(",", ""))
    if college_row is None:
        for i in range(22):
            data_row_list.append("")
    else:
        #data_row_list.append(college_row.find(attrs={"data-stat": ""}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "season"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "g"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "mp"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fga_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg_pct"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg2_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg2a_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg2_pct"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg3_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg3a_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fg3_pct"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "ft_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "fta_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "ft_pct"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "trb_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "ast_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "stl_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "blk_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "tov_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "pf_per_min"}).text)
        data_row_list.append(college_row.find(attrs={"data-stat": "pts_per_min"}).text)

    # Add NBA stats
    data_row_list.append("NBA")
    data_row_list.append(nba_row.find(attrs={"data-stat": "g"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "mp"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "pts"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "trb"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "ast"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "fg_pct"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "fg3_pct"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "ft_pct"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "mp_per_g"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "pts_per_g"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "trb_per_g"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "ast_per_g"}).text)

    # Blocks and steals (per 36)
    data_row_list.append(player_combined_dict['blocks_per_36'])
    data_row_list.append(player_combined_dict['steals_per_36'])
    #data_row_list.append("")
    #data_row_list.append("")

    data_row_list.append(nba_row.find(attrs={"data-stat": "ws"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "ws_per_48"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "bpm"}).text)
    data_row_list.append(nba_row.find(attrs={"data-stat": "vorp"}).text)

    data_row_list.append(player_combined_dict['bbref'])


    return name, data_row_list


def get_scout_data(nba_stats_dict, year):

    # Get page
    scout_url = constants.recruit_url.format(year)
    scout_page = requests.get(scout_url)
    scout_soup = BeautifulSoup(scout_page.text, 'lxml')

    # Get table with data
    scout_table = scout_soup.find('div', id='div_rsci_rankings')
    rankings_dict = dict()
    for player in nba_stats_dict.keys():
        player_cell = scout_table.find(text=player)
        if player_cell != None:
            scout_ranking = player_cell.parent.parent.parent.find(attrs={'data-stat': 'rank'}).text
            rankings_dict[player] = scout_ranking
        else:
            rankings_dict[player] = ""

    return rankings_dict


def get_nba_career_data(player_combined_dict):
    # TODO: figure out how to handle edge cases better.
    if player_combined_dict['bbref'] is None or player_combined_dict['bbref'] == "":
        player_combined_dict['blocks_per_36'] = ""
        player_combined_dict['steals_per_36'] = ""
        return None
    url = constants.bbref_base_url + player_combined_dict['bbref']
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    per_minute_table_comment = soup.find(text=lambda text: text and isinstance(text, Comment) and 'Per 36 Minutes Table' in text)
    if per_minute_table_comment is None:
        player_combined_dict['blocks_per_36'] = ""
        player_combined_dict['steals_per_36'] = ""
        return None

    per_minute_soup = BeautifulSoup(per_minute_table_comment, 'lxml')

    career_stats_row = per_minute_soup.find('tfoot').find('tr')
    player_combined_dict['blocks_per_36'] = career_stats_row.find(attrs={'data-stat': 'blk_per_mp'}).text
    player_combined_dict['steals_per_36'] = career_stats_row.find(attrs={'data-stat': 'stl_per_mp'}).text

    return None


def scrape():

    # Open file, write headers
    file = open("data.csv", 'w')
    for header in constants.stats_header:
        file.write(header)
        file.write(',')
    file.write('\n')

    for year in constants.years:
        year_str = str(year)
        logger.info("Starting gathering data for {}".format(year_str))

        #TODO: Need to make it so that all the data goes into this dict, keyed off player name.
        all_data_dict = dict()

        # Get list of players (and nba stats)
        # Get the web page for the draft year
        draft_page = requests.get(constants.draft_url.format(year_str))
        soup = BeautifulSoup(draft_page.text, 'lxml')

        # Find the rows of data on players
        draft_table = soup.find('div', class_="table_outer_container")
        rows = draft_table.find('tbody')
        rows_list = rows.find_all('tr')
        nba_stats_dict = dict()
        for row in rows_list:
            try:
                if not row.find(attrs={'aria-label': "Player"}) and not row.find(attrs={'data-stat': 'header_per_g'}):
                    name, data = format_nba_data(row)
                    nba_stats_dict[name] = row
                    all_data_dict[name] = {'draft_page_row': row}
                    try:
                        player_link = row.find(attrs={'data-stat': 'player'}).find('a')
                        web_link = player_link['href']
                        all_data_dict[name]['bbref'] = web_link
                    except:
                        all_data_dict[name]['bbref'] = None
                    get_nba_career_data(all_data_dict[name])

            except Exception as e:
                pass

        # Get ages... ugh
        # Get the web page
        second_draft_page = requests.get(constants.extended_draft_url.format(year_str))
        soup = BeautifulSoup(second_draft_page.text, 'lxml')

        # Get the rows from the table corresponding to the players we have
        second_draft_table = soup.find('div', class_="table_outer_container")
        second_rows = second_draft_table.find('tbody')
        second_rows_list = second_rows.find_all('tr')
        age_dict = dict()
        for row in second_rows_list:
            try:
                if not row.find(attrs={'aria-label': "Player"}) and not row.find(attrs={'data-stat': 'header_per_g'}):
                    name = row.find(attrs={'data-stat': 'player'}).text
                    age = row.find(attrs={'data-stat': 'age'}).text
                    age_dict[name] = age
                    all_data_dict[name]['age'] = age
            except:
                pass

        # Get college stats
        college_stats_dict = dict()
        height_dict = dict()
        college_position_dict = dict()
        for player in nba_stats_dict:
            # If there is no college entry on the NBA page, don't try to get data
            # (likely an international player)
            if nba_stats_dict[player].find(attrs={"data-stat": "college_name"}).text == "":
                college_stats_dict[player] = None
                height_dict[player] = ""
                college_position_dict[player] = ""
                all_data_dict[player]["college_stats"] = None
                all_data_dict[player]['height'] = ""
                all_data_dict[player]['position'] = ""
            else:
                try:
                    college_data_dict = get_college_data(player, year_str, 1)
                    stats_row = college_data_dict['recent_season']
                    height = college_data_dict['height']
                    position = college_data_dict['position_formatted']
                except Exception as e:
                    # Something went wrong here. Just ignore and move on.
                    logger.error("failed to get college data for {0}".format(player))
                    logger.error(e)
                    stats_row = None
                    height = ""
                    position = ""

                all_data_dict[player]['college_stats'] = stats_row
                all_data_dict[player]['height'] = height
                all_data_dict[player]['position'] = position
                college_stats_dict[player] = stats_row
                height_dict[player] = height
                college_position_dict[player] = position

        # Get scout's consensus
        #TODO: Figure out how to do this efficiently/accurately
        #rankings_dict = get_scout_data(nba_stats_dict, year)
        rankings_dict = {}

        # append all stats
        all_stats = list()
        for player in nba_stats_dict:
            name, data_list = format_for_csv(nba_stats_dict[player], college_stats_dict[player], age_dict[player], height_dict[player], college_position_dict[player], all_data_dict[player], year_str)
            all_stats.append(data_list)

        # write year's stats to file
        for player_list in all_stats:
            write_line = ""
            for value in player_list:
                write_line += str(value)
                write_line += ","
            write_line.rstrip(',')
            write_line += "\n"
            file.write(write_line)

    # Cleanup
    file.close()
    return None


if __name__ == "__main__":
    if "data.csv" in os.listdir(os.getcwd()):
        os.remove(os.getcwd() + "/data.csv")
    scrape()
