import requests
from bs4 import BeautifulSoup
import teams

def get_team_lengths(url):
    name_lengths = list()

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table')
    rows = table.find('tbody').find_all('tr')

    for row in rows:
        name = row.find('th').text
        name_lengths.append(len(name))

    return name_lengths

def pick_winner(team1, team2):
    team1_name, team1_url = team1
    team2_name, team2_url = team2

    t1l = get_team_lengths(team1_url)
    t2l = get_team_lengths(team2_url)

    t1_avg = float(sum(t1l))/len(t1l)
    t2_avg = float(sum(t2l))/len(t2l)

    if t1_avg < t2_avg:
        return "{0}: {1}<{2}".format(team1_name, t1_avg, t2_avg)
    elif t2_avg < t1_avg:
        return "{0}: {1}<{2}".format(team2_name, t2_avg, t1_avg)
    else:
        return 'TIE {0}:{1}  :: {2}:{3}'.format(team1_name, t1_avg, team2_name, t2_avg)

if __name__ == '__main__':
    # print(pick_winner(teams.virginia, teams.umbc))
    # print(pick_winner(teams.creighton, teams.kansasstate))
    # print(pick_winner(teams.kentucky, teams.davidson))
    # print(pick_winner(teams.arizona, teams.buffalo))
    # print(pick_winner(teams.miami, teams.loyola))
    # print(pick_winner(teams.tennessee, teams.wright))
    # print(pick_winner(teams.nevada, teams.texas))
    # print(pick_winner(teams.cinci, teams.georgia))
    # print("------------------------------")
    # print(pick_winner(teams.xavier, teams.texassouthern))
    # print(pick_winner(teams.missouri, teams.floridastate))
    # print(pick_winner(teams.ohiostate, teams.sdstate))
    # print(pick_winner(teams.gonzaga, teams.ncgreen))
    # print(pick_winner(teams.houston, teams.sandstate))
    # print(pick_winner(teams.michigan, teams.montana))
    # print(pick_winner(teams.taam, teams.providence))
    # print(pick_winner(teams.unc, teams.linscomb))
    print(pick_winner(teams.vil, teams.radford))
    print(pick_winner(teams.virtec, teams.alabama))
    print(pick_winner(teams.westvirg, teams.murray))
