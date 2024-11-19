import requests 
import json

def get_puuid(api_key, nickname, tagline):
    match_base_url = "https://americas.api.riotgames.com"
    url = f"{match_base_url}/riot/account/v1/accounts/by-riot-id/{nickname}/{tagline}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data["puuid"]
    else:
        return None

def get_match_history(api_key, puuid, count=5):
    match_base_url = "https://americas.api.riotgames.com"
    url = f"{match_base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_match_details(api_key, match_id):
    match_base_url = "https://americas.api.riotgames.com"
    url = f"{match_base_url}/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": api_key
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

