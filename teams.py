from nba_api.stats.endpoints import commonteamroster, leaguedashteamstats, teaminfocommon, commonplayerinfo, teamplayerdashboard
import concurrent.futures
from nba import getCurrentSeasonStats
import pandas as pd

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

    head_coach = head_coach.to_dict(orient='records')[0]
    team_roster = team_roster.to_dict(orient='records')

    return {'teamRoster': team_roster, 'headCoach': head_coach}




