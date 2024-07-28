import mysql.connector
from mysql.connector import Error
import json
from src.tokenRemover import replaceDash

visitedTeams = set()
with open('../playerBase1.json') as file:
    data = json.load(file)

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='lhlosdb',
                                         user='root',
                                         password='ellinas123')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
    
player_insert_query = '''
INSERT INTO player (Name, Position, Ethnicity, Photo)
VALUES (%s, %s, %s, %s)
'''

for item in data:
    name = item.get('Name')
    position = item.get('Position')
    ethnicity = item.get('Ethnicity')
    photo = item.get('Photo')
    cursor.execute(player_insert_query, (name, position, ethnicity, photo))

    
squads_insert_query = '''
INSERT INTO Squads 
VALUES (%s, %s, %s)
'''
team_select_query = '''
SELECT id FROM Team WHERE name = (%s) 
'''

playerIndex = 0

for item in data:
    playerIndex += 1 
    stats = item.get('Stats', {})
    for year, details in stats.items():
        team = details.get("Team")
        cursor.execute(team_select_query, (team,))
        teamId = cursor.fetchone()
        cursor.execute(squads_insert_query, (year, teamId[0], playerIndex))
        
team_insert_query = '''
INSERT INTO Team (name, logo)
VALUES (%s, %s)
'''
visitedTeams = set()

for item in data:
    stats = item.get('Stats', {})
    for year, details in stats.items():
        team_name = details.get("Team")
        if team_name and team_name not in visitedTeams:
            visitedTeams.add(team_name)
            logo = item.get('Photo')
            cursor.execute(team_insert_query, (team_name, logo))


squads_insert_query = '''
INSERT INTO Stats
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
playerIndex = 0

for item in data:
    playerIndex += 1
    stats = item.get('Stats', {})
    for year, details in stats.items():
        seasonStats = details.get("Stats")
        cursor.execute(squads_insert_query, (playerIndex, year, replaceDash(seasonStats[0]),replaceDash(seasonStats[1]),replaceDash(seasonStats[2]),replaceDash(seasonStats[3]),replaceDash(seasonStats[5]),replaceDash(seasonStats[6]),replaceDash(seasonStats[7]),replaceDash(seasonStats[8]),replaceDash(seasonStats[9]),replaceDash(seasonStats[10]),replaceDash(seasonStats[13]),replaceDash(seasonStats[14]),replaceDash(seasonStats[15]),replaceDash(seasonStats[16]),replaceDash(seasonStats[18])))


connection.commit()
    

if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")