from nba_api.stats.endpoints import commonteamroster, leaguedashteamstats, teaminfocommon, commonplayerinfo, teamplayerdashboard, teamgamelog
import concurrent.futures
from nba import getCurrentSeasonStats
import pandas as pd
import numpy as np
import math

def getTeamStats(team_id):
    team_id = int(team_id)
    ls = leaguedashteamstats.LeagueDashTeamStats().get_data_frames()[0]
    ls = ls[ls['TEAM_ID'] == team_id]

    return ls.to_dict(orient='records')[0]

def getTeamInfo(team_id):
    team_id = int(team_id)
    cti = teaminfocommon.TeamInfoCommon(team_id).get_data_frames()[0]

    return cti.to_dict(orient='records')[0]

def getPlayerStatus(player_id):
    try:
        return commonplayerinfo.CommonPlayerInfo(player_id).get_data_frames()[0].to_dict(orient='records')[0]['ROSTERSTATUS']
    except Exception as e:
        print(f"Error fetching status for player {player_id}: {e}")
        return "Unknown"

def getTeamRoster(team_id):
    get_roster = commonteamroster.CommonTeamRoster(team_id).get_data_frames()
    player_stats = teamplayerdashboard.TeamPlayerDashboard(team_id).get_data_frames()[1]

    team_roster = get_roster[0]
    head_coach = get_roster[1]

    head_coach = head_coach[head_coach['COACH_TYPE'] == 'Head Coach']
    team_roster = pd.merge(team_roster, player_stats, on='PLAYER_ID')

    team_roster['GP'] = team_roster['GP'].replace(0, 1)

    team_roster['PPG'] = round(team_roster['PTS'] / team_roster['GP'], 2)
    team_roster['RPG'] = round(team_roster['REB'] / team_roster['GP'], 2)
    team_roster['APG'] = round(team_roster['AST'] / team_roster['GP'], 2)

    try:
        head_coach = head_coach.to_dict(orient='records')[0]
    except IndexError:
        head_coach = {'COACH_ID': "None", 'COACH_NAME': "None"}
    team_roster = team_roster.to_dict(orient='records')

    if head_coach['SORT_SEQUENCE'] and math.isnan(head_coach['SORT_SEQUENCE']):
        head_coach['SORT_SEQUENCE'] = 'NULL'

    return {'teamRoster': team_roster, 'headCoach': head_coach}

def teamColors(team_id: int):
    colors = {
        "1610612737": {"abb":"ATL","colors":{"1":"#E03A3E","2":"#C1D32F","3":"#26282A"}},
        "1610612738": {"abb":"BOS","colors":{"1":"#007A33","2":"#BA9653","3":"#963821"}},
        "1610612739": {"abb":"CLE","colors":{"1":"#860038","2":"#041E42","3":"#FDBB30"}},
        "1610612740": {"abb":"NOP","colors":{"1":"#0C2340","2":"#C8102E","3":"#85714D"}},
        "1610612741": {"abb":"CHI","colors":{"1":"#CE1141","2":"#000000"}},
        "1610612742": {"abb":"DAL","colors":{"1":"#00538C","2":"#002B5E","3":"#B8C4CA"}},
        "1610612743": {"abb":"DEN","colors":{"1":"#0E2240","2":"#FEC524","3":"#8B2131"}},
        "1610612744": {"abb":"GSW","colors":{"1":"#1D428A","2":"#FFC72C"}},
        "1610612745": {"abb":"HOU","colors":{"1":"#CE1141","2":"#000000","3":"#C4CED4"}},
        "1610612746": {"abb":"LAC","colors":{"1":"#C8102E","2":"#1D428A","3":"#BEC0C2"}},
        "1610612747": {"abb":"LAL","colors":{"1":"#552583","2":"#FDB927","3":"#000000"}},
        "1610612748": {"abb":"MIA","colors":{"1":"#98002E","2":"#F9A01B","3":"#000000"}},
        "1610612749": {"abb":"MIL","colors":{"1":"#00471B","2":"#EEE1C6","3":"#0077C0"}},
        "1610612750": {"abb":"MIN","colors":{"1":"#0C2340","2":"#236192","3":"#9EA2A2"}},
        "1610612751": {"abb":"BKN","colors":{"1":"#000000","2":"#FFFFFF"}},
        "1610612752": {"abb":"NYK","colors":{"1":"#006BB6","2":"#F58426","3":"#BEC0C2"}},
        "1610612753": {"abb":"ORL","colors":{"1":"#0077C0","2":"#C4CED4","3":"#000000"}},
        "1610612754": {"abb":"IND","colors":{"1":"#002D62","2":"#FDBB30","3":"#BEC0C2"}},
        "1610612755": {"abb":"PHI","colors":{"1":"#006BB6","2":"#ED174C","3":"#002B5C"}},
        "1610612756": {"abb":"PHX","colors":{"1":"#1D1160","2":"#E56020","3":"#000000"}},
        "1610612757": {"abb":"POR","colors":{"1":"#E03A3E","2":"#000000"}},
        "1610612758": {"abb":"SAC","colors":{"1":"#5A2D81","2":"#63727A","3":"#000000"}},
        "1610612759": {"abb":"SAS","colors":{"1":"#C4CED4","2":"#000000"}},
        "1610612760": {"abb":"OKC","colors":{"1":"#007AC1","2":"#EF3B24","3":"#002D62"}},
        "1610612761": {"abb":"TOR","colors":{"1":"#CE1141","2":"#000000","3":"#A1A1A4"}},
        "1610612762": {"abb":"UTA","colors":{"1":"#002B5C","2":"#00471B","3":"#F9A01B"}},
        "1610612763": {"abb":"MEM","colors":{"1":"#5D76A9","2":"#12173F","3":"#F5B112"}},
        "1610612764": {"abb":"WAS","colors":{"1":"#002B5C","2":"#E31837","3":"#C4CED4"}},
        "1610612765": {"abb":"DET","colors":{"1":"#C8102E","2":"#1D42BA","3":"#BEC0C2"}},
        "1610612766": {"abb":"CHA","colors":{"1":"#1D1160","2":"#00788C","3":"#A1A1A4"}}
        }


    
    return colors[team_id]

#Index(['Team_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'W', 'L', 'W_PCT',
#       'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
#       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
#       'PTS'],
#      dtype='object')

def getTeamGameLog(team_id: int):
    # Get regular season and playoff logs
    regular_log = teamgamelog.TeamGameLog(team_id=team_id).get_data_frames()[0]
    playoff_log = teamgamelog.TeamGameLog(team_id=team_id, season_type_all_star="Playoffs").get_data_frames()[0]

    # Combine the two
    combined_log = pd.concat([regular_log, playoff_log], ignore_index=True)

    # Convert 'GAME_DATE' to datetime
    combined_log['GAME_DATE'] = pd.to_datetime(combined_log['GAME_DATE'], format='%b %d, %Y')

    # Sort by date descending
    combined_log = combined_log.sort_values(by='GAME_DATE', ascending=False).reset_index(drop=True)

    return combined_log.to_dict(orient='records')




