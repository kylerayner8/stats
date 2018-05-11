import requests
import time
import re

from bs4 import BeautifulSoup
from functools import lru_cache

def get_soup(url, logger):
    try:
        time.sleep(1)
        wpage = requests.get(url)
        re.compile("<!--|-->")
        soup = BeautifulSoup(re.sub("<!--|-->","", wpage.text), 'lxml')

        return soup

    except Exception as e:
        logger.error(e)
        raise


@lru_cache(maxsize=256)
def get_soup_cache(url, logger):
    return get_soup(url, logger)


def get_data_from_draft_page_row(player_row, data_type, logger):
    try:
        return player_row.find('td', attrs={'data-stat':data_type})

    except Exception as e:
        logger.error(e)
        raise


def test_json(row, logger):
    try:
        d = dict()
        for item in row.find_all('td'):
            key = item['data-stat']
            val = item.text
            d[key] = val

        return d

    except Exception as e:
        logger.error(e)
        raise


# TODO: Better exception messages. 
def get_tables_from_sportsref_page(ref_soup, logger, college=False):
    try:
        if college:
            table_class = "table_wrapper"
        else:
            table_class = "table_container"
        tables = ref_soup.find_all('div', class_=table_class)
        stats_dict = dict()
        for table_div in tables:
            table = table_div.find(lambda tag: tag.name=='table')
            table_name = table['id']
            table_dict = dict()
            if table.find('tbody') != None:
                for row in table.find('tbody').find_all('tr'):
                    row_title = row.get('id', None)
                    row_dict = dict()
                    if row_title != None:
                        for stat in row.find_all('td'):
                            row_dict[stat['data-stat']] = stat.text
                            link = stat.find('a')
                            if link:
                                row_dict[stat['data-stat']+'_link'] = link['href']
                        if table_dict.get(row_title, None) != None:
                            #TODO: For players who were traded/played on different teams
                            # in a year, this breaks. All rows for a year have the same
                            # title. Need to figure out something with the classes.
                            logger.error("Overwriting row! {}".format(row_title))
                        table_dict[row_title] = row_dict
            if stats_dict.get(table_name, None) != None:
                logger.error("Overwriting table! {}".format(table_name))
            stats_dict[table_name] = table_dict

        return stats_dict

    except Exception as e:
        logger.error(e, exc_info=True)
        raise