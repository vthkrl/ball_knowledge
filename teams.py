from nba_api.stats.endpoints import commonteamroster, leaguedashteamstats, teaminfocommon, commonplayerinfo
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

def getTeamRoster(team_id):
    get_roster = commonteamroster.CommonTeamRoster(team_id).get_data_frames()

    team_roster = get_roster[0]
    head_coach = get_roster[1]

    head_coach = head_coach[head_coach['COACH_TYPE'] == 'Head Coach']

    team_roster = team_roster.to_dict(orient='records') #List of dictionaries
    head_coach = head_coach.to_dict(orient='records')[0] #Dictionary

    return {'teamRoster': team_roster, 'headCoach': head_coach}



getTeamRoster(1610612747)


