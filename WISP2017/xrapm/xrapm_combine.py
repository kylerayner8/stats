import write_csv

years_dict_list = list()
order = ["name", "2015xrapm", "2015oxrapm", "2015dxrapm",
         "2014xrapm", "2014oxrapm", "2014dxrapm",
         "2013xrapm", "2013oxrapm", "2013dxrapm",
         "2012xrapm", "2012oxrapm", "2012dxrapm",
         "2011xrapm", "2011oxrapm", "2011dxrapm",
         "2010xrapm", "2010oxrapm", "2010dxrapm",
         "2009xrapm", "2009oxrapm", "2009dxrapm",
         "2008xrapm", "2008oxrapm", "2008dxrapm",
         "2007xrapm", "2007oxrapm", "2007dxrapm",
         "2006xrapm", "2006oxrapm", "2006dxrapm",
         "2005xrapm", "2005oxrapm", "2005dxrapm"]

full_dict = dict()
for i in range(5, 16):
    year = 2000+i
    filename = "{0}.txt".format(year)
    file = open(filename, 'r')
    for line in file.readlines():
        items = line.strip('\n').split(',')
        name = items[0]
        oxrapm = items[1]
        dxrapm = items[2]
        xrapm = items[3]
        player_dict = full_dict.get(name, dict())
        player_dict['name'] = name
        player_dict[str(year) + "oxrapm"] = oxrapm
        player_dict[str(year) + "dxrapm"] = dxrapm
        player_dict[str(year) + "xrapm"] = xrapm
        full_dict[name] = player_dict

players_list = list()
for key in full_dict:
    players_list.append(full_dict[key])

write_csv.write_csv(players_list, "full_xrapm.csv", order)

