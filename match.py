import json
import requests
import pandas as pd
from time import sleep

api_key = "RGAPI-70faa0cc-7a6f-4d8c-9ef0-a790d1bd776e"   

csv = pd.read_csv('Game_id.csv', encoding="UTF-8")  
temp = csv['Game_id']   

match = []	

for i in range(len(temp)):	
    try:
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + temp[i]
        res = requests.get(URL, headers={"X-Riot-Token": api_key})
        resobj = json.loads(res.text)
        win_experience = 0
        lose_experience = 0
        win_goldspent = 0
        lose_goldspent = 0

        for j in range(10):
            if resobj["info"]["participants"][j]["win"] == False:
                if resobj["info"]["participants"][j]["teamPosition"] == "TOP" :
                    top_l = resobj["info"]["participants"][j]["championName"]
                elif resobj["info"]["participants"][j]["teamPosition"] == "MIDDLE" :
                    middle_l = resobj["info"]["participants"][j]["championName"]
                elif resobj["info"]["participants"][j]["teamPosition"] == "JUNGLE" :
                    jungle_l = resobj["info"]["participants"][j]["championName"]
                elif resobj["info"]["participants"][j]["teamPosition"] == "BOTTOM" :
                    bottom_l = resobj["info"]["participants"][j]["championName"]
                else :
                    utility_l = resobj["info"]["participants"][j]["championName"]
                lose_experience = lose_experience + resobj["info"]["participants"][j]["champExperience"]
                lose_goldspent = lose_experience + resobj["info"]["participants"][j]["goldSpent"]
            else :
                if resobj["info"]["participants"][j]["teamPosition"] == "TOP" :
                    top_w = resobj["info"]["participants"][j]["championName"]
                elif resobj["info"]["participants"][j]["teamPosition"] == "MIDDLE" :
                    middle_w = resobj["info"]["participants"][j]["championName"]
                elif resobj["info"]["participants"][j]["teamPosition"] == "JUNGLE" :
                    jungle_w = resobj["info"]["participants"][j]["championName"]
                elif resobj["info"]["participants"][j]["teamPosition"] == "BOTTOM" :
                    bottom_w = resobj["info"]["participants"][j]["championName"]
                else :
                    utility_w = resobj["info"]["participants"][j]["championName"]
                win_experience = win_experience + resobj["info"]["participants"][j]["champExperience"]
                win_goldspent = lose_experience + resobj["info"]["participants"][j]["goldSpent"]
        win_team = [top_w,middle_w,jungle_w,bottom_w,utility_w,"Win",win_experience,win_goldspent]
        lose_team = [top_l,middle_l,jungle_l,bottom_l,utility_l,"Lose",lose_experience,lose_goldspent]

        if (resobj["info"]["teams"][0]["win"]==True):
            win_team.append(resobj["info"]["teams"][0]["objectives"]["baron"]["kills"])
            win_team.append(resobj["info"]["teams"][0]["objectives"]["champion"]["kills"])
            win_team.append(resobj["info"]["teams"][0]["objectives"]["dragon"]["kills"])
            win_team.append(resobj["info"]["teams"][0]["objectives"]["inhibitor"]["kills"])
            win_team.append(resobj["info"]["teams"][0]["objectives"]["riftHerald"]["kills"])
            win_team.append(resobj["info"]["teams"][0]["objectives"]["tower"]["kills"])
            win_team.append(resobj["info"]["teams"][0]["teamId"])
            lose_team.append(resobj["info"]["teams"][1]["objectives"]["baron"]["kills"])
            lose_team.append(resobj["info"]["teams"][1]["objectives"]["champion"]["kills"])
            lose_team.append(resobj["info"]["teams"][1]["objectives"]["dragon"]["kills"])
            lose_team.append(resobj["info"]["teams"][1]["objectives"]["inhibitor"]["kills"])
            lose_team.append(resobj["info"]["teams"][1]["objectives"]["riftHerald"]["kills"])
            lose_team.append(resobj["info"]["teams"][1]["objectives"]["tower"]["kills"])
            lose_team.append(resobj["info"]["teams"][1]["teamId"])
        else:
            win_team.append(resobj["info"]["teams"][1]["objectives"]["baron"]["kills"])
            win_team.append(resobj["info"]["teams"][1]["objectives"]["champion"]["kills"])
            win_team.append(resobj["info"]["teams"][1]["objectives"]["dragon"]["kills"])
            win_team.append(resobj["info"]["teams"][1]["objectives"]["inhibitor"]["kills"])
            win_team.append(resobj["info"]["teams"][1]["objectives"]["riftHerald"]["kills"])
            win_team.append(resobj["info"]["teams"][1]["objectives"]["tower"]["kills"])
            win_team.append(resobj["info"]["teams"][1]["teamId"])
            lose_team.append(resobj["info"]["teams"][0]["objectives"]["baron"]["kills"])
            lose_team.append(resobj["info"]["teams"][0]["objectives"]["champion"]["kills"])
            lose_team.append(resobj["info"]["teams"][0]["objectives"]["dragon"]["kills"])
            lose_team.append(resobj["info"]["teams"][0]["objectives"]["inhibitor"]["kills"])
            lose_team.append(resobj["info"]["teams"][0]["objectives"]["riftHerald"]["kills"])
            lose_team.append(resobj["info"]["teams"][0]["objectives"]["tower"]["kills"])
            lose_team.append(resobj["info"]["teams"][0]["teamId"])

        match.append(win_team)
        match.append(lose_team)

        print(f"Processed game {i+1}/{len(temp)}")
    except:
        continue
    if (i+1)%100 == 0 :
        sleep(3)
        
df = pd.DataFrame(match, columns=['TOP','MIDDLE','JUNGLE','BOTTOM','UTILITY','OUTCOME','experience','goldspent','baron','champion_kills','dragon','inhibitor','riftHerald','tower','teamId'])
df.to_csv('match.csv', index=False, encoding='utf-8')