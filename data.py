"""
data loader
"""

imenaDatotek = """fivb_world_championship_2010.txt
fivb_world_championship_standings.txt
fivb_world_cup_2011.txt
fivb_world_cup_head_to_head_21-Oct-2011.txt
fivb_world_cup_standings.txt
fivb_world_league_2010.txt
fivb_world_league_2011.txt
fivb_world_league_2012.txt
fivb_world_league_head_to_head_03-Jun-2010.txt
fivb_world_league_head_to_head_16-May-2012.txt
fivb_world_league_head_to_head_27-May-2011.txt
fivb_world_league_standings.txt
fivb_world_league_statistics_03-Jun-2010.txt
fivb_world_league_statistics_16-May-2012.txt
fivb_world_league_statistics_27-May-2011.txt
fivb_world_ranking_02-Oct-2011.txt
fivb_world_ranking_04-Jan-2012.txt
fivb_world_ranking_15-Jan-2010.txt
fivb_world_ranking_15-Jan-2011.txt
fivb_world_ranking_27-Jul-2010.txt
""".strip().split("\n")

def getData():
    return {ime : [i.strip().split("\t") for i in open("data/"+ime).readlines()] for ime in imenaDatotek}



a = getData()

for i,j in a.items():
    if i.startswith("fivb_world_league_head_to_head"):
        print j
        
        
        
        
        
        