from nba_api.stats.endpoints import leagueleaders
import pandas as pd

def getLeagueLeaders(category):
    ll = leagueleaders.LeagueLeaders().get_data_frames()[0]

    per_game_stats = {
        'PPG': 'PTS',
        'RPG': 'REB',
        'APG': 'AST',
        'SPG': 'STL',
        'BPG': 'BLK',
        '3PMPG': 'FG3M',
        '3PAPG': 'FG3A',
        'FTMPG': 'FTM',
        'FTAPG': 'FTA',
        'FGMPG': 'FGM',
        'MINPG': 'MIN'
    }

    if category in per_game_stats:
        ll = ll[ll['GP'] > 0].copy()

        ll[category] = (ll[per_game_stats[category]] / ll['GP']).round(1)

        data = ll.sort_values(category, ascending = False)

        return data.to_dict(orient = 'records')

    data = ll.sort_values(category, ascending = False)

    return data.to_dict(orient='records')
