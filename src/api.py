import requests

def get_puuid(nickname, tagline):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nickname}/{tagline}"
    headers = {
        "X-Riot-Token": "RGAPI-a9767604-ede1-4525-ad25-607c65f149a7"
    }
    response = requests.get(url, headers=headers)
    pass    

def get_match_history(puuid, count=5):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {
        "X-Riot-Token": "RGAPI-a9767604-ede1-4525-ad25-607c65f149a7"
    }
    response = requests.get(url, headers=headers)
    pass

def get_match_details(match_id):
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": "RGAPI-a9767604-ede1-4525-ad25-607c65f149a7"
    }
    response = requests.get(url, headers=headers)
    pass