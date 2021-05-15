# ./leaguepedia_scraping.py 
# This script requests information on every competitive games played on the patches 11.1 to 11.9 
# to the Leaguepedia API, using MWClient & Cargo 
"""
TODO : 
    The current code is not working as it should : requests results are limited to 500 results per request
    which means we have to split the big requests on much smaller requests to build our database.
"""
from db import *
from var import *
import mwclient
import json 
from time import sleep

# Focusing on season 11 patches because I lack storage
"""PATCH_LIST = [
    "11.1",
    "11.2",
    "11.3",
    "11.4",
    "11.5",
    "11.6",
    "11.7",
    "11.8",
    "11.9"
]
PATCH_LIST = [
    "11.2"
]"""
if __name__ == "__main__":
    # Using mwclient to connect to the Leaguepedia API
    site = mwclient.Site('lol.fandom.com', path='/')
    continuer=True
    date="2021-04-01 00:00:00" 
    stocklongueur=500
    # Creating a where clause for my specific patches
    while(continuer):
        sleep(2)

        where_clause="SG.DateTime_UTC >= '"+date+"'" #Version sans patch

        #A décommenter si on veut choisir les patchs
        """where_clause = "SG.DateTime_UTC >= '"+date+"' AND ("
        for i in range(len(PATCH_LIST)):
            where_clause += f'SG.Patch="{PATCH_LIST[i]}"' if i==len(PATCH_LIST)-1 else f'SG.Patch="{PATCH_LIST[i]}" OR '
        where_clause+=")"""
        
        print(where_clause)


        # Request
        response = site.api('cargoquery', 
            limit = 'max',
            tables = "ScoreboardGames=SG",
            fields = "SG.Team1, SG.Team2, SG.Patch, SG.MatchHistory, SG.DateTime_UTC, SG.Tournament, SG.WinTeam",
            where = where_clause,
            order_by="SG.DateTime_UTC"
        )
        
        json_data = json.loads(json.dumps(response))
        
        
        # Printing teams, patch and match history link for every game

        connection=create_connection(host_name,user_name,user_password,database_name,host_port) #Connect to BDD

        for row in json_data['cargoquery']:
            try:
                #print(row)
                addGame(connection,row) #Add game to BDD
            except:
                print("Error")
        longueur=len(json_data['cargoquery'])
        
        #print(longueur)

        if(longueur==0 or (stocklongueur!=500 and stocklongueur==longueur)):
            continuer=False
        else:
            date=json_data['cargoquery'][longueur-1]["title"]["DateTime UTC"]
            #print(date)
        stocklongueur=longueur
