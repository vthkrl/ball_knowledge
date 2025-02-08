from nba_live import getBoxscore

def getPlayerPerf(p_id, game_id):
    game_box = getBoxscore(game_id)

    t = game_box['homeTeam']['players'] + game_box['awayTeam']['players']

    player = [p for p in t if str(p['personId']) == str(p_id)][0]

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
        '+/-': player['statistics']['plusMinusPoints']
    }, 
    player['name'],
    gd]

    return stats
