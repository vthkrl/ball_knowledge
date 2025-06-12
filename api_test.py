import pandas as pd
from player_performances import getPlayerGameLog
from teams import getTeamGameLog
import json
from nba_api.stats.endpoints import playercareerstats

st = playercareerstats.PlayerCareerStats(2544).get_data_frames()[0]

print(st)