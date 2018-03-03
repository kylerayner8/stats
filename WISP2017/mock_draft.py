import os
import requests
from bs4 import BeautifulSoup
from write_csv import write_csv

base_url = "http://www.spotrac.com/nba/{}/yearly/cap/"
order = ['name', 'pos', 'age', '16', '17', '18', '19', '20']


def get_team_salaries(team_name):
    #file = open(os.getcwd()+"/team_salaries/"+team_name+".csv", 'w')
    page = requests.get(base_url.format(team_name))
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', class_="responsive")
    rows = table.find('tbody').find_all('tr')

    salary_info_list = list()

    first_year = 16
    for row in rows:
        player_dict = dict()
        cols = row.find_all('td')
        player_dict['name'] = cols[0].text
        player_dict['pos'] = cols[1].text
        player_dict['age'] = cols[2].text
        for i in range(5):
            year = str(first_year+i)
            salary = cols[i+3].text.replace(",", "").lstrip("$")

            if "UFA" in salary:
                salary = "UFA"
            elif "RFA" in salary:
                salary = "RFA"
            elif salary == "0-":
                salary = ""
            player_dict[year] = salary

        salary_info_list.append(player_dict)

    write_csv(salary_info_list, "{0}.csv".format(team_name), order)
    #file.close()
    return None

if __name__ == "__main__":
    get_team_salaries("washington-wizards")
