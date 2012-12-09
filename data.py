"""
data loader
"""

from collections import defaultdict

def split(line):
    while line.find("  ") != -1:
        line = line.replace("  "," ")
    return line.replace("\t"," ").strip().split(" ")

def vrniDatum(datum):
    mes = {"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}
    datum = datum.split("-")
    return int(datum[2] + mes[datum[1]] + datum[0])
    
def vrniStand():
    standings = """
    fivb_world_championship_standings.txt
    fivb_world_cup_standings.txt
    fivb_world_league_standings.txt
    """.strip().split("\n")
    result = {}
    for ime in standings:
        ime = ime.strip()
        f = open("data/"+ime)
        dIme = ime[11:-14] #.replace("fivb_world_","").replace("_standings.txt","")
        head = split(f.readline())
        stand = [split(i) for i in f.readlines()]
        country = {}
        for i,vrstica in enumerate(stand):
            d = {int(head[j]+"1231") : vrstica[j] for j in range(2, len(vrstica))}
            d["N"] = vrstica[1]
            country[vrstica[0]] = d
        result[dIme] = country
    return result


def vrniHead():
    filenames = """
    fivb_world_league_head_to_head_03-Jun-2010.txt
    fivb_world_league_head_to_head_27-May-2011.txt
    fivb_world_cup_head_to_head_21-Oct-2011.txt
    fivb_world_league_head_to_head_16-May-2012.txt
    """.strip().split("\n")

    result = defaultdict(lambda : defaultdict(dict))

    for file in filenames:
        ime = file.strip() 
        f = open("data/"+ime)
        datum = vrniDatum(ime[-15:-4])        
        glava = split(f.readline())[1:]
        lines = [split(i) for i in f.readlines()]
        for line in lines:
            for i, element in enumerate(line[1:]):
                result[line[0]][datum][glava[i]] = element
            
    return result



def vrniRank():
    ranking = """
    fivb_world_ranking_15-Jan-2010.txt
    fivb_world_ranking_27-Jul-2010.txt
    fivb_world_ranking_15-Jan-2011.txt
    fivb_world_ranking_02-Oct-2011.txt
    fivb_world_ranking_04-Jan-2012.txt
    """.strip().split("\n")
    
    result = defaultdict(dict)
    
    for ime in ranking:
        ime = ime.strip()
        f = open("data/"+ime)
        datum = vrniDatum(ime[-15:-4])
        rank = [split(i) for i in f.readlines()][1:]
        for vrstica in rank:
            result[vrstica[1]][datum] = {"Points" : vrstica[2], "Rank" : vrstica[0]}

    return result


def vrniStat():
    statistics = """
    fivb_world_league_statistics_03-Jun-2010.txt
    fivb_world_league_statistics_27-May-2011.txt
    fivb_world_league_statistics_16-May-2012.txt
    """.strip().split("\n")
    
    result = defaultdict(lambda : defaultdict(dict))
    
    for ime in statistics:
        ime = ime.strip()
        f = open("data/"+ime)
        datum = vrniDatum(ime[-15:-4])
        glava = split(f.readline())[1:]
        lines = [split(i) for i in f.readlines()]
        for line in lines:
            for i, element in enumerate(line[1:]):
                result[line[0]][datum][glava[i]] = element
    return result


def vrniTekme():
    tekme = """
    fivb_world_championship_2010.txt
    fivb_world_league_2010.txt
    fivb_world_league_2011.txt
    fivb_world_cup_2011.txt
    fivb_world_league_2012.txt
    """.strip().split("\n")
    
    result = defaultdict(list)
    
    for ime in tekme:
        ime = ime.strip()
        f = open("data/"+ime)
        imeT = ime.replace("fivb_world_","").split("_")[0]
        glava = split(f.readline())
        lines = [split(i) for i in f.readlines()]
        for line in lines:
            line[2] = vrniDatum(line[2])
            result[imeT].append({glava[i] : el for i, el in enumerate(line)})
    
    return result

tekme = vrniTekme()
stat = vrniStat()
rank = vrniRank()
head = vrniHead()
stand = vrniStand()

#def urediTekmo(tekma):
    
    

















