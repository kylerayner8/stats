from wisp2018.data_scraping.utilities import get_soup, get_soup_cache, get_tables_from_sportsref_page

def get_college_stats(url, logger):
    try:

        college_soup = get_soup(url, logger)
        all_college_stats = get_tables_from_sportsref_page(college_soup, logger)

        # Also get pace info from team page
        # Used cache soup-er for these pages, could be hitting
        # multiple times
        for year_stats_key in all_college_stats['players_per_game']:
            year_stats = all_college_stats['players_per_game'][year_stats_key]
            school_url = year_stats.get('school_name_link', None)
            if school_url != None:
                school_url = "http://www.sports-reference.com" + school_url
                team_soup = get_soup_cache(school_url, logger)
                team_info = team_soup.find('div', id='info', class_='schools')

                psg = team_info.find(lambda x: x.name == 'p' and 'PS/G' in x.text)
                pag = team_info.find(lambda x: x.name == 'p' and 'PA/G' in x.text)
                sos = team_info.find(lambda x: x.name == 'p' and 'SOS' in x.text)
                srs = team_info.find(lambda x: x.name == 'p' and 'SRS' in x.text)
                
                psg_str = psg.text.split(":")[1].split("(")[0].strip()
                pag_str = pag.text.split(":")[1].split("(")[0].strip()
                srs_str = srs.text.split(":")[1].split("(")[0].strip()
                sos_str = sos.text.split(":")[1].split("(")[0].strip()

                year_stats['ps_per_g'] = psg_str
                year_stats['pa_per_g'] = pag_str
                year_stats['srs'] = srs_str
                year_stats['sos'] = sos_str

        return all_college_stats

    except Exception as e:
        logger.error("Problem getting college stats for {0}: {1}".format(url, e), exc_info=True)