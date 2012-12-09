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

def jeZmagal(tekma, ekipa):
    rez = map(int, tekma["Result"].split('-'))
    ind = rez.index(max(rez))
    
    return int(ekipa == tekma["Teams"].split('-')[ind])

def getRazmirje(ekipa, datum):
    flat = tekme['league'] + tekme['championship'] + tekme['cup']
    flat = [i for i in flat if i['Date'] < datum]
    flat = [i for i in flat if ekipa in set(i['Teams'].split('-')) ]
    
    zmage = [jeZmagal(i, ekipa) for i in flat]
    
    return float(sum(zmage))/len(zmage)


def getRangZmage(ekipa, datum):
    flat = tekme['league'] + tekme['championship'] + tekme['cup']
    flat = [i for i in flat if i['Date'] < datum]
    flat = [i for i in flat if ekipa in set(i['Teams'].split('-')) ]
    
    tocke_w = 0
    tocke_l = 0
    for tekma in flat:
        nEkipa = set(tekma['Teams'].split('-'))
        nEkipa.remove(ekipa)
        nEkipa = nEkipa.pop()
        nTocke = float(sorted([(d,i) for d, i in rank[nEkipa].items() if d <= datum ])[-1][1]["Points"])
        tocke_w += nTocke if jeZmagal(tekma, ekipa) == 1  else 0
        tocke_l += 0 if jeZmagal(tekma, ekipa) == 1  else nTocke
    
    return (tocke_w, tocke_l)

def getSteviloTekem(ekipa, datum):    
    flat = tekme['league'] + tekme['championship'] + tekme['cup']
    flat = [i for i in flat if i['Date'] < datum]
    flat = [i for i in flat if ekipa in set(i['Teams'].split('-')) ]
        
    return len(flat)

def zmagalZadnjo(ekipa, nEkipa, datum):
    flat = tekme['league'] + tekme['championship'] + tekme['cup']
    
    flat = [i for i in flat if i['Date'] < datum]
    flat = [i for i in flat if set(i['Teams'].split('-')) == set([ekipa, nEkipa])]
    
    flat = sorted(flat, key = lambda x : x['Date'])
    
    zadna  = flat[-1]
    return jeZmagal(zadna, ekipa)

def getAllKeys():
    keys = set()
    for s in stat.values():
        for d, el in s.items():
            for name in el.keys():
                keys.add("stat-%d-%s" % (d,name))
    
    for r in rank.values():
        for d, el in r.items():
            for name in el.keys():
                keys.add("rank-%d-%s" % (d,name))
    
    
    for d, el in head["ARG"].items():
        for name in el.keys():
            keys.add("head-%d-%s" % (d,name))

    
    for imeTekmovanja, std in stand.items():
        for ekipa in std.keys():
            for d, el in std[ekipa].items():
                keys.add("standings-%s-%s" % (imeTekmovanja, str(d)))

    keys.add("rank-points-sum")
    keys.add("rank-rank-sum")
    
    keys.add("head-zmage")
    keys.add("head-zgube")

    keys.add("zmagal-zadnjo")
    keys.add("razmerje-zmag")
    keys.add("stevilo-tekem")
    
    keys.add("rank-zmage-points")
    keys.add("rank-zgube-points")
    keys.add("rank-razmerje-points")
                
    return keys

def getTeamData(ekipa, nEkipa, datum):
    
    teamD = {}
    for d, el in stat[ekipa].items():
        for name, item in el.items():
            teamD["stat-%d-%s" % (d,name)] = item if d <= datum else "-"
    
    for d, el in rank[ekipa].items():
        for name, item in el.items():
            teamD["rank-%d-%s" % (d,name)] = item if d <= datum else "-"
        
    for d, el in head[ekipa].items():
        for name, item in el.items():
            teamD["head-%d-%s" % (d,name)] = item if d <= datum else "-"
    
    for imeTekmovanja, std in stand.items():
        if ekipa in std:
            for d, el in std[ekipa].items():
                teamD["standings-%s-%s" % (imeTekmovanja, str(d))] = el if d <= datum else "-"
    
    teamD["rank-points-sum"] = sum([float(i["Points"]) for d,i in rank[ekipa].items() if d < datum])
    teamD["rank-rank-sum"] = sum([int(i["Rank"]) for d,i in rank[ekipa].items() if d < datum])
    

    #st zmag proti ekipi
    
    teamD["head-zmage"] = sum([int(j) for d, el in head[ekipa].items() for i,j in el.items() if d <= datum if i == "%s_W" % (nEkipa)])
    teamD["head-zgube"] = sum([int(j) for d, el in head[ekipa].items() for i,j in el.items() if d <= datum if i == "%s_L" % (nEkipa)])
    

    teamD["zmagal-zadnjo"] = zmagalZadnjo(ekipa, nEkipa, datum)
    teamD["razmerje-zmag"] = getRazmirje(ekipa, datum)
    teamD["stevilo-tekem"] = getSteviloTekem(ekipa, datum)
    
    tockeW, tockeL = getRangZmage(ekipa, datum)
    teamD["rank-zmage-points"] = tockeW
    teamD["rank-zgube-points"] = tockeL
    teamD["rank-razmerje-points"] = tockeW - tockeL
    
    return teamD
    
def urediTekmo(tekma):
    team = tekma["Teams"].split("-")
    datum = tekma["Date"]
    
    teamA = getTeamData(team[0], team[1], datum)
    teamB = getTeamData(team[1], team[0], datum)

    
    line = [teamA[k] for k in keys] + [teamB[k] for k in keys]
    
    line.append(tekma['Audience'])
    line.append(tekma['Host'] == team[0])
    line.append(tekma['Host'] == team[1])
    line.append(tekma['Date'])
    
    r = map(int,tekma['Result'].split('-'))
    res = [jeZmagal(tekma, team[0]) , r[0]-r[1]]
    
    lines = []
    result = []
    lines.append(list(line))
    result.append()
    
    print keys
    print line
    print result
    return lines , result






tekme = vrniTekme()
stat = vrniStat()
rank = vrniRank()
head = vrniHead()
stand = vrniStand()

keys = sorted(getAllKeys())

