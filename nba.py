from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerawards
import pandas as pd

#['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 
# 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 
# 'TOV', 'PF', 'PTS']

def getImage(p_id: int):
    image = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{p_id}.png'
    
    return image

def getCareerStats(p_id: int):
    career = playercareerstats.PlayerCareerStats(player_id = p_id)
    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK']
    career_stats = {}
    
    for cat in categories: #add career total PTS, REB, AST, STL, BLK
        career_stats.update({cat : career.get_data_frames()[1][cat].iloc[0]})

    return career_stats

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

def comparePlayers(p1: str, p2: str):
    p1_id = players.find_players_by_full_name(p1)[0]['id']
    p2_id = players.find_players_by_full_name(p2)[0]['id']

    career1 = getCareerStats(p1_id)
    career2 = getCareerStats(p2_id)

    award1 = getAwards(p1_id)
    award2 = getAwards(p2_id)

    career1.update(award1)
    career2.update(award2)

    images = [getImage(p1_id), getImage(p2_id)]

    data = {
        p1: career1,
        p2: career2
    }

    df = pd.DataFrame(data)

    return [df, images]

