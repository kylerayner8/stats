import requests
import os
from bs4 import BeautifulSoup
from write_csv import write_csv

rpm_base_url = "http://www.espn.com/nba/statistics/rpm/_/year/{0}/page/{1}"
years = [2017, 2016, 2015, 2014]
header_order = [
    'name',
    #'position',
    '2017gp',
    '2017mp',
    '2017rpm',
    '2017orpm',
    '2017drpm',
    '2016gp',
    '2016mp',
    '2016rpm',
    '2016orpm',
    '2016drpm',
    '2015gp',
    '2015mp',
    '2015rpm',
    '2015orpm',
    '2015drpm',
    '2014gp',
    '2014mp',
    '2014rpm',
    '2014orpm',
    '2014drpm',
]

def get_rpm():

    rpm_list = list()
    rpm_dict = dict()
    for year in [2017, 2016, 2015, 2014]:
        for index in range(12):
            page = requests.get(rpm_base_url.format(year, index))
            soup = BeautifulSoup(page.text, 'lxml')
            table = soup.find('table', class_="tablehead")
            if table is not None:
                oddrows = table.find_all("tr", class_="oddrow")
                evenrows = table.find_all("tr", class_="evenrow")
                all_rows = oddrows + evenrows
                for row in all_rows:
                    columns = row.find_all('td')
                    identity = columns[1].text.split(", ")
                    name = identity[0]
                    position = identity[1]
                    team = columns[2].text
                    gp = columns[3].text
                    mpg = columns[4].text
                    orpm = columns[5].text
                    drpm = columns[6].text
                    rpm = columns[7].text
                    wins = columns[8].text

                    player_dict = rpm_dict.get(name, dict())
                    player_dict['name'] = name
                    #player_dict['position'] = position
                    player_dict[str(year)+'gp'] = gp
                    player_dict[str(year)+'rpm'] = rpm
                    player_dict[str(year)+'orpm'] = orpm
                    player_dict[str(year)+'drpm'] = drpm
                    player_dict[str(year) + 'mp'] = mpg
                    #player_dict[str(year)+'wins'] = wins

                    rpm_dict[name] = player_dict

    for player_key in rpm_dict:
        rpm_list.append(rpm_dict.get(player_key, []))

    return rpm_list

rpm_list = get_rpm()
write_csv(rpm_list, 'rpm_full.csv', order=header_order)