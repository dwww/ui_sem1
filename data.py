"""
data loader
"""

standings = """
fivb_world_championship_standings.txt
fivb_world_cup_standings.txt
fivb_world_league_standings.txt
""".strip().split("\n")

head = """
fivb_world_league_head_to_head_03-Jun-2010.txt
fivb_world_league_head_to_head_27-May-2011.txt
fivb_world_cup_head_to_head_21-Oct-2011.txt
fivb_world_league_head_to_head_16-May-2012.txt
""".strip().split("\n")

statistics = """
fivb_world_league_statistics_03-Jun-2010.txt
fivb_world_league_statistics_27-May-2011.txt
fivb_world_league_statistics_16-May-2012.txt
""".strip().split("\n")

ranking = """
fivb_world_ranking_15-Jan-2010.txt
fivb_world_ranking_27-Jul-2010.txt
fivb_world_ranking_15-Jan-2011.txt
fivb_world_ranking_02-Oct-2011.txt
fivb_world_ranking_04-Jan-2012.txt
""".strip().split("\n")

tekme = """
fivb_world_championship_2010.txt
fivb_world_league_2010.txt
fivb_world_league_2011.txt
fivb_world_cup_2011.txt
fivb_world_league_2012.txt
""".strip().split("\n")


def presipaj(fun, ind):
    tab = fun
    for i in tab:
        for j in i:
            tmp = []
            for n in ind:
                tmp = tmp + [j[n]] 
            j = tmp
            print j

def vrniStand():
    
    stand = [[i.strip().split(" ") for i in open("data/"+ime).readlines()] for ime in standings]
        
    for i in range(len(stand)): #s pomikanjem po tabeli se teza podatkov niza
        stand[i] = stand[i][1:len(stand)]
        for j in range(len(stand[i])):
            for n in range(len(stand[i][j])):
                if "-" in stand[i][j][n]: stand[i][j][n] = "-1" #iz - spremeni v -1 
            print stand[i][j]
    return stand


def vrniHead():
    
    heads = [[i.strip().split(" ") for i in open("data/"+ime).readlines()] for ime in head]

    for i in heads:
        i = i[1:len(i)]
        for j in i:
            print j
    return heads


def vrniRank():

    rank = [[i.strip().split("\t") for i in open("data/"+ime).readlines()] for ime in ranking]
        
    for i in rank:
        i = i[1:len(i)]
        for j in i:
            print j
    return rank


def vrniStat():
   
    stat = [[i.strip().split(" ") for i in open("data/"+ime).readlines()] for ime in statistics]
    
    for i in stat:
        i = i[1:len(i)]
        for j in i:
            print j
    return stat


def vrniTekme():

    pod = [[i.strip().split("\t") for i in open("data/"+ime).readlines()] for ime in tekme]
    
    for i in range(len(pod)):
        pod[i] = pod[i][1:len(pod[i])]
        for j in range(len(pod[i])):
            for n in range(len(pod[i][j])):
                if "-" in pod[i][j][n]: pod[i][j][n] = pod[i][j][n].split("-")
                if "NA" in pod[i][j][n]: pod[i][j][n] = ["0","0"] #namesto rezultata NA da 0 : 0  
            
            pod[i][j] = pod[i][j][3:11] 
            print pod[i][j]
    return pod

#presipaj(vrniStand(), range(5))