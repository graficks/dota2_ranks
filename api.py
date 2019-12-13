import requests
import time
import csv
response = requests.get("https://api.opendota.com/api/publicMatches")
public_match_data = response.json()
print(len(public_match_data))
rank_wl = []
account_ids = []
with open('player_ranks.csv', mode='a') as player_file:
    file_writer = csv.writer(player_file, delimiter=',')
    for x in range(100):
        try:
            response2 = requests.get("https://api.opendota.com/api/matches/{}".format(public_match_data[x].get('match_id')) )
            time.sleep(1)
            match_id = response2.json()
            players = match_id.get('players')
            curr = []
            for y in range(len(players)):
                if(players[y].get('account_id')!=None):
                    account_ids.append(players[y].get('account_id'))
                    curr.append(players[y].get('account_id'))
            #print(account_ids)
            print("---")
            for each in curr:
                response3 = requests.get("https://api.opendota.com/api/players/{}".format(each))
                time.sleep(1)
                response4 = requests.get("https://api.opendota.com/api/players/{}/wl".format(each))
                time.sleep(1)
                r3 = response3.json()
                print("rank_tier: " + str(r3.get('rank_tier')))
                print(response4.json())
                print("---")
                if(len(response4.json()) != 2):
                    print("error rate")
                    break
                rank_wl.append([r3.get('rank_tier'), response4.json().get('win'), response4.json().get('lose') ] )
                if(r3.get('rank_tier') == 'None'):
                    tier = 0
                else:
                    tier = r3.get('rank_tier')
                file_writer.writerow([each, tier, response4.json().get('win'), response4.json().get('lose')])
            #print(rank_wl)
            print("count:")
            print(x)
        except:
            print("except")
            break
