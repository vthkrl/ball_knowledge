from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.static import players
from datetime import time, timezone
from dateutil import parser
import pandas as pd

def getTodayGames():
    board = scoreboard.ScoreBoard()
    data = board.get_dict()
    games = []

    for game in data['scoreboard']['games']:
        games.append({
            'gameId': game['gameId'],
            'away_team': game['awayTeam']['teamName'],
            'home_team': game['homeTeam']['teamName'],
            'away_team_id': game['awayTeam']['teamId'],
            'home_team_id': game['homeTeam']['teamId'],
            'away_score': game['awayTeam']['score'],
            'home_score': game['homeTeam']['score'],
            'period': game['period'],
            'time_left': game['gameClock'] if game['gameStatusText'] == "In Progress" else game['gameStatusText']
        })

    return games

def getBoxscore(game_id):
    if type(game_id) is not str:
        game_id = str(game_id)
    box = boxscore.BoxScore(game_id=game_id)

    gameDetails = box.game_details.get_dict()
    location = box.arena.get_dict()
    homeTeam = box.home_team.get_dict()
    awayTeam = box.away_team.get_dict()

    pack = {
        'gameDetails': gameDetails,
        'location': location,
        'homeTeam': homeTeam,
        'awayTeam': awayTeam,
    }

    return pack
