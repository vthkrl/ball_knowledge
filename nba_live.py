from nba_api.live.nba.endpoints import scoreboard
from datetime import datetime, timezone
from dateutil import parser

f = '{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}'

board = scoreboard.ScoreBoard()
print("Date:", board.score_board_date)
games = board.games.get_dict()
for game in games:
    gameTimeLTZ = parser.parse(game['gameTimeUTC']).replace(tzinfo=timezone.utc).astimezone(tz=None)
    print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))
