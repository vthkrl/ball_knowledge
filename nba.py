from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import drafthistory
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerawards
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguestandings
import pandas as pd

#['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 
# 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 
# 'TOV', 'PF', 'PTS']

def leagueStandings():
    ls = leaguestandings.LeagueStandings().get_data_frames()[0]
    west = []
    east = []

    west_leader = ls[ls['Conference'] == 'West'].nlargest(1, 'WINS').iloc[0]
    east_leader = ls[ls['Conference'] == 'East'].nlargest(1, 'WINS').iloc[0]

    for _, row in ls.iterrows():
        gb = (west_leader['WINS'] - row['WINS'] + row['LOSSES'] - west_leader['LOSSES']) / 2 if row['Conference'] == 'West' else \
             (east_leader['WINS'] - row['WINS'] + row['LOSSES'] - east_leader['LOSSES']) / 2
        
        team_data = {
            'teamId': row['TeamID'],
            'teamCity': row['TeamCity'],
            'teamName': row['TeamName'],
            'conference': row['Conference'],
            'playoffRank': row['PlayoffRank'],
            'record': f"{row['WINS']} - {row['LOSSES']}",
            'wins': row['WINS'],
            'losses': row['LOSSES'],
            'winPct': row['WinPCT'],
            'GB': gb if gb > 0 else 0.0
        }

        if row['Conference'] == 'West':
            west.append(team_data)
        else:
            east.append(team_data)

    return {'east': east, 'west': west}



def getDraftHistory(p_id: int):
    draft = drafthistory.DraftHistory().get_data_frames()[0]
    df_draft = draft[draft['PERSON_ID'] == p_id]
    player_draft = {
        'Draft Year': df_draft['SEASON'],
        'Draft Round': df_draft['ROUND_NUMBER'],
        'Pick Number': df_draft['ROUND_PICK'],
        'Draft Team': df_draft['TEAM_NAME']
    }

    return player_draft
    
def getPlayerImage(p_id: int):
    image = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{p_id}.png'
    
    return image

def getCareerStats(p_id: int):
    career = playercareerstats.PlayerCareerStats(player_id = p_id)
    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK']
    career_stats = {}
    
    for cat in categories: #add career total PTS, REB, AST, STL, BLK
        career_stats.update({cat : int(career.get_data_frames()[1][cat].iloc[0])})

    ppg = round(career.get_data_frames()[1]['PTS']/career.get_data_frames()[1]['GP'], 1)

    career_stats.update({'PPG': ppg[0]})

    return career_stats

def getCurrentSeasonStats(p_id: int):
    season = playercareerstats.PlayerCareerStats(player_id = p_id).get_data_frames()[0].iloc[-1]
    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK']
    season_stats = {}

    ppg = round(season['PTS']/season['GP'], 1)
    rpg = round(season['REB']/season['GP'], 1)
    apg = round(season['AST']/season['GP'], 1)
    spg = round(season['STL']/season['GP'], 1)
    bpg = round(season['BLK']/season['GP'], 1)

    season_stats.update({'PPG': ppg})
    season_stats.update({'RPG': rpg})
    season_stats.update({'APG': apg})
    season_stats.update({'SPG': spg})
    season_stats.update({'BPG': bpg})

    for cat in categories:
        season_stats.update({cat: int(season[cat])})

    return season_stats

def getAwards(p_id: int):
    awards = playerawards.PlayerAwards(player_id= p_id).get_data_frames()[0]
    career_awards = {}
    categories = {'Championships': 'Champion',
                  'Finals MVPs': 'KFMVP',
                  'MVPs': 'KIMVP',  
                  'DPOYs': 'KDPYR', 
                  'All-NBA': 'KIANT', 
                  'All-Defensive': 'KIADT',
                  'All-Star': 'All-Star'
                  }
    
    for award in categories.keys():
        filtered_awards_st1 = awards[awards['SUBTYPE1'] == categories[award]]
        filtered_awards_st2 = awards[awards['SUBTYPE2'] == categories[award]]

        count = len(filtered_awards_st1) + len(filtered_awards_st2)

        career_awards.update({award: count})

    return career_awards

def comparePlayers(p1: str, p2: str, stats_type: str):
    p1_id = players.find_players_by_full_name(p1)[0]['id']
    p2_id = players.find_players_by_full_name(p2)[0]['id']

    if stats_type == 'career':
        career1 = getCareerStats(p1_id)
        career2 = getCareerStats(p2_id)

        award1 = getAwards(p1_id)
        award2 = getAwards(p2_id)

        career1.update(award1)
        career2.update(award2)

    else:
        career1 = getCurrentSeasonStats(p1_id)
        career2 = getCurrentSeasonStats(p2_id)

    images = [getPlayerImage(p1_id), getPlayerImage(p2_id)]

    data = {
        p1: career1,
        p2: career2
    }

    df = pd.DataFrame(data)

    return [df, images]

def getTeamLogo(team_id: int):
    image = f'https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg'

    return image

