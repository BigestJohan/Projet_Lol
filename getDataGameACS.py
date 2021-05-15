
from db import *
from var import *
import requests
import json


connection=create_connection(host_name,user_name,user_password,database_name,host_port)

listgames=getlinksGame(connection)
#print(len(listgames))

listgames.reverse()
base_match_history_stats_url = "https://acs.leagueoflegends.com/v1/stats/game/{}/{}?{}"
base_match_history_stats_timeline_url = "https://acs.leagueoflegends.com/v1/stats/game/{}/{}/timeline?{}"

#listgamesub=listgames[0:1]
getlistalreadydone=getGamesAlreadyImport(connection)
listalreadydone=[]
for done in getlistalreadydone:
    listalreadydone.append(done[0])



listnotdone=[]
x=0
for game in listgames: #listgamesub
    gameurl=game[0]
    x+=1
    if(x%1000==0):
        print(x)
    if(gameurl not in listalreadydone):
        if("http://matchhistory" in gameurl or "https://matchhistory" in gameurl): 
            try:
                splitgame=gameurl.split("/")
                gameinfo=splitgame[6]
                gameinfosplit=gameinfo.split("?")
                gameId=gameinfosplit[0]
                hash=gameinfosplit[1]
                server=splitgame[5]
                url = base_match_history_stats_url.format(server,gameId,hash)
                timeline_url = base_match_history_stats_timeline_url.format(server,gameId,hash)

                print(gameurl,url,timeline_url)
                
                game_data = requests.get(url,  cookies={c.split("=")[0]:c.split("=")[1] for c in cookies.split(";")}).json()
                game_datatimeline= requests.get(timeline_url,  cookies={c.split("=")[0]:c.split("=")[1] for c in cookies.split(";")}).json()
                #print(len(str(game_data)),len(str(game_datatimeline)))

                addData(connection,json.dumps(game_data),json.dumps(game_datatimeline),gameurl)
            except:
                print("Error parsing 'matchhistory'"+gameurl)
        else:
            listnotdone.append(gameurl)

print(listnotdone,len(listnotdone))

connection.close();
