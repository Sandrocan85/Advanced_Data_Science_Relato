import os
import requests
import time
import json

def load_API_key(file_path):
    with open (file_path, "r") as file:
        return file.read().strip()

RIOT_API_KEY=load_API_key("C:/Users/Alessandro Relato/Desktop/Uni/terzo anno/Advanced data science/Riot Developer Key.txt")
request_counter=0

def get_challenger_players(region="euw1"):
    url=f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    headers={"X-Riot-Token": RIOT_API_KEY}
    
    while(1):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429: 
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit raggiunto. Attesa di {retry_after} secondi...")
            time.sleep(retry_after)
        else:
            print(f"Errore: {response.status_code}, {response.text}")
            return None

def get_timelines(match_id, region="europe"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    headers={"X-Riot-Token": RIOT_API_KEY}
    
    while(1):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429: 
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit raggiunto. Attesa di {retry_after} secondi...")
            time.sleep(retry_after)
        else:
            print(f"Errore: {response.status_code}, {response.text}")
            return None

def get_piuud(summoner_id, region="euw1"):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    
    while(1):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429: 
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit raggiunto. Attesa di {retry_after} secondi...")
            time.sleep(retry_after)
        else:
            print(f"Errore: {response.status_code}")
            print(f"{response.json()}")
            return None

def get_match_ids(puuid, region="europe", start=50, count=100):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {"start": start, "count": count, "queue": 420}  # Start e Count definiscono l'intervallo, queue: 420 per selezionare solo le Ranked Solo/Duo
    headers = {"X-Riot-Token": RIOT_API_KEY}
    
    while(1):
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429: 
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit raggiunto. Attesa di {retry_after} secondi...")
            time.sleep(retry_after)
        else:
            print(f"Errore: {response.status_code}")
            print(f"{response.json()}")
            return None

def get_match_details(match_id, region="europe"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    
    while(1):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429: 
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit raggiunto. Attesa di {retry_after} secondi...")
            time.sleep(retry_after)
        else:
            print(f"Errore: {response.status_code}")
            print(f"{response.json()}")
            return None


summoners=get_challenger_players()
"""
with open("summoners.json", "r") as file:
    summoners=json.load(file)
"""
matches=[]
"""
with open("matches.json", "r") as file:
    matches=json.load(file)
"""
players=summoners["entries"]
for summoner in players:
    summoner["puuid"]=get_piuud(summoner["summonerId"])["puuid"]
    matches.append(get_match_ids(summoner["puuid"], count=20, start=10))

summoners["entries"]=players

with open("summoners.json", "w") as file:
    json.dump(summoners, file, indent=4)

with open("matches.json", "w") as file:
    json.dump(matches, file, indent=4)

matches_info=[]
for summoner in matches:
    for match_id in summoner:
        matches_info.append(get_match_details(match_id))

timelines=[]
conta=1
for summoner in matches:
    for match_id in summoner:
        timelines.append(get_timelines(match_id))
        if len(timelines)==5:
            with open("timelines/timelines_"+str(conta)+".json", "w") as file:
                json.dump(timelines, file, indent=4)
            timelines=[]
            conta+=1


with open("matches_info.json", "w") as file:
    json.dump(matches_info, file, indent=4)

