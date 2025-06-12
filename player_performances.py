from nba_api.stats.endpoints import playergamelog
from nba_live import getBoxscore
from datetime import datetime
import pandas as pd

def getPlayerPerf(p_id, game_id):
    game_box = getBoxscore(game_id)

    home_players = game_box['homeTeam']['players']
    away_players = game_box['awayTeam']['players']

    all_players = home_players + away_players

    # Find the player
    player = [p for p in all_players if str(p['personId']) == str(p_id)][0]

    # Determine the player's team
    if any(str(p['personId']) == str(p_id) for p in home_players):
        team_info = {
            'teamName': game_box['homeTeam']['teamName'],
            'teamId': game_box['homeTeam']['teamId'],
            'teamSide': 'home'
        }
    else:
        team_info = {
            'teamName': game_box['awayTeam']['teamName'],
            'teamId': game_box['awayTeam']['teamId'],
            'teamSide': 'away'
        }

    gd = {
        'gameId': game_box['gameDetails']['gameId'],
        'gameStatusText': game_box['gameDetails']['gameStatusText'],
        'gameTimeUTC': game_box['gameDetails']['gameTimeUTC'],
        'awayTeam': game_box['awayTeam']['teamName'],
        'awayTeamId': game_box['awayTeam']['teamId'],
        'awayTeamScore': game_box['awayTeam']['score'],
        'homeTeam': game_box['homeTeam']['teamName'],
        'homeTeamId': game_box['homeTeam']['teamId'],
        'homeTeamScore': game_box['homeTeam']['score']
    }

    stats = [{
        'MIN': player['statistics']['minutesCalculated'],
        'PTS': player['statistics']['points'],
        'REB': player['statistics']['reboundsTotal'],
        'AST': player['statistics']['assists'],
        'STL': player['statistics']['steals'],
        'BLK': player['statistics']['blocks'],
        'FGM': player['statistics']['fieldGoalsMade'],
        'FGA': player['statistics']['fieldGoalsAttempted'],
        '3PM': player['statistics']['threePointersMade'],
        '3PA': player['statistics']['threePointersAttempted'],
        'FTM': player['statistics']['freeThrowsMade'],
        'FTA': player['statistics']['freeThrowsAttempted'],
        '+/-': player['statistics']['plusMinusPoints'],
        'teamName': team_info['teamName'],
        'teamId': team_info['teamId'],
        'teamSide': team_info['teamSide']
    }, 
    player['name'],
    gd, team_info]

    return stats

#Index(['SEASON_ID', 'Player_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 'WL',
#       'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
#       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
#       'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE'],
#      dtype='object')
def getPlayerGameLog(p_id: int):
    regular_log = playergamelog.PlayerGameLog(player_id=p_id).get_data_frames()[0]
    playoff_log = playergamelog.PlayerGameLog(player_id=p_id, season_type_all_star="Playoffs").get_data_frames()[0]

    combined_log = pd.concat([regular_log, playoff_log], ignore_index=True)

    combined_log['GAME_DATE'] = pd.to_datetime(combined_log['GAME_DATE'], format='%b %d, %Y')

    combined_log = combined_log.sort_values(by='GAME_DATE', ascending=False).reset_index(drop=True)

    return combined_log.to_dict(orient='records')