import json
import csv

with open("Matches_info.json", "r") as file:
    matches_info=json.load(file)

nodes=[]
nodes_set=set()
edges=[]
edges_set=set()

# 1200 file, 4 match per file
n_file=1
n_match=0
# Passa ogni file delle timeline
while(n_file<1201):
    name="timelines/timelines_"+str(n_file)+".json"
    print("Analyzing file "+name, end=" ")
    with open(name) as file:
        timelines=json.load(file)
    n_match=0
    # Passa ogni game in ogni file delle timeline
    while(n_match<4):
        # Salva le info generali
        timeline=timelines[n_match]
        metadata=timeline["metadata"]
        info=timeline["info"]
        participants={}
        # Cerca il match in matches_info che corrispondo a quello in analisi dalle timeline
        match=next((item for item in matches_info if item["metadata"]["matchId"] == metadata["matchId"]), None)
        if match==None:
            continue
        else:
            # Crea una lista di dizionari che rappresentano i nodi e un dizionazio con i partecipanti a questa partita
            n_participant=0
            n_p=0
            for participant in metadata["participants"]:
                if participant not in nodes_set:
                    nodes_set.add(participant)
                    nodes.append({"id": participant,
                                  "role": match["info"]["participants"][n_participant]["teamPosition"],
                                  "name": match["info"]["participants"][n_participant]["summonerName"]})
                    n_participant+=1
                participants[n_p]=participant
                n_p+=1
            # Cerco gli eventi relativi alle kill di campioni, mostri epici e torri
            for frame in info["frames"]:
                events=[e for e in frame["events"] if e["type"]=="CHAMPION_KILL"] # Filtra solo gli eventi di CHAMPIO_KILL
                if events==None:
                    continue
                else:
                    # Per ogni evento prende chi ha fatto la kill e la lista con gli assist, li trasforma in puuid e li mette nella lista e nel set degli archi se non ci sono
                    # o aumenta il peso se ci sono già
                    for event in events:
                        if "assistingParticipantIds" in event:
                            killer=participants[event["killerId"]-1]
                            assists=event["assistingParticipantIds"]
                            for assistId in assists:
                                assistId_right=participants[assistId-1]
                                if (killer, assistId_right) not in edges_set and (assistId_right, killer) not in edges_set:
                                    edges_set.add((killer, assistId_right))
                                    edges.append({"source": killer,
                                                "target": assistId_right,
                                                "weight": 1})
                                else:
                                    existing_edge = next((edge for edge in edges if (edge['source'] == killer and edge['target'] == assistId_right) or (edge['target'] == killer and edge['source'] == assistId_right)), None)
                                    if existing_edge:
                                        existing_edge["weight"]+=1
                                # Poi crea anche l'arco con l'assistman successivo (se è l'ultimo lo crea con il primo)
                                if len(assists)>1:
                                    index=assists.index(assistId)+1
                                    if index>=len(assists):
                                        index=0
                                    else:
                                        index=assists.index(assistId)+1
                                    otherId=participants[assists[index]-1]
                                    if (otherId, assistId_right) not in edges_set and (otherId, assistId_right) not in edges_set:
                                        edges_set.add((otherId, assistId_right))
                                        edges.append({"source": otherId,
                                                    "target": assistId_right,
                                                    "weight": 1})
                                    else:
                                        existing_edge = next((edge for edge in edges if (edge['source'] == otherId and edge['target'] == assistId_right) or (edge['target'] == otherId and edge['source'] == assistId_right)), None)
                                        if existing_edge:
                                            existing_edge["weight"]+=1
        n_match+=1
        print(". ", end="")
    n_file+=1
    print("")
# Salva i file dei nodi e degli archi
with open("nodes.csv", "w", newline='', encoding="utf-8") as file:
    writer=csv.DictWriter(file, fieldnames=["id", "role", "name"])
    writer.writeheader()
    writer.writerows(nodes)
with open("edges.csv", "w", newline='', encoding="utf-8") as file:
    writer=csv.DictWriter(file, fieldnames=["source", "target", "weight"])
    writer.writeheader()
    writer.writerows(edges)
print("Finito!")