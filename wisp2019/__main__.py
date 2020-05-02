from wisp2019.collection.scraper import get_nba_data_for_draft_year
from wisp2019.collection.utilities import get_soup_cache
print("Running WISP!")

# TODO: Logging and data directory cleanup/setup each time this runs?
for yr in range(2011, 2020):
    get_nba_data_for_draft_year(yr, write=True)
    print(get_soup_cache.cache_info())
