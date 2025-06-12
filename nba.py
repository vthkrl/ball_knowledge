from nba_api.stats.endpoints import playercareerstats, leaguestandings, drafthistory, playerawards, commonplayerinfo
from nba_api.stats.static import players, teams
from datetime import datetime
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

def getCurrentSeasonStats(p_id):
    try:
        player_stats_df = playercareerstats.PlayerCareerStats(player_id=p_id).get_data_frames()[0]

        if player_stats_df.empty:
            return {"PPG": 0.00, "RPG": 0.00, "APG": 0.00, "SPG": 0.00, "BPG": 0.00}

        # Determine the current NBA season string (e.g., "2024-25")
        today = datetime.today()
        year = today.year
        if today.month >= 10:  # NBA season typically starts in October
            current_season = f"{year}-{str(year + 1)[-2:]}"
        else:
            current_season = f"{year - 1}-{str(year)[-2:]}"

        # Filter to the current season only
        current_season_df = player_stats_df[player_stats_df['SEASON_ID'] == current_season]

        if current_season_df.empty:
            return {"PPG": 0.00, "RPG": 0.00, "APG": 0.00, "SPG": 0.00, "BPG": 0.00}

        season = current_season_df.iloc[0]

        return {
            "PPG": round(season.get("PTS", 0) / max(season.get("GP", 1), 1), 2),
            "RPG": round(season.get("REB", 0) / max(season.get("GP", 1), 1), 2),
            "APG": round(season.get("AST", 0) / max(season.get("GP", 1), 1), 2),
            "SPG": round(season.get("STL", 0) / max(season.get("GP", 1), 1), 2),
            "BPG": round(season.get("BLK", 0) / max(season.get("GP", 1), 1), 2)
        }
    except Exception as e:
        print(f"Error fetching stats for player {p_id}: {e}")
        return {"PPG": 0.00, "RPG": 0.00, "APG": 0.00, "SPG": 0.00, "BPG": 0.00}

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

def getPlayerInfo(p_id: int):
    info = commonplayerinfo.CommonPlayerInfo(p_id).get_data_frames()[0]

    return info

def constructPlayerBio(p_id: int):
    common_info = getPlayerInfo(p_id)
    stats = getCurrentSeasonStats(p_id)

    return {'info': common_info, 'stats': stats}

def gmsc(PTS: int, FG: int, FGA: int, FTA: int, FT: int, ORB: int, DRB: int, STL: int, AST: int, BLK: int, PF: int, TOV: int) -> int:
    return int(round(PTS + 0.4 * FG - 0.7 * FGA - 0.4 * (FTA - FT) + 0.7 * ORB + 0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV))
#great idea i just had: write a function that looks at a bunch of games
#and uses some sort of metric to find some of the
#best performances from that set of games
#this could be good for finding the highlight performances from,
#for example, a playoff series

