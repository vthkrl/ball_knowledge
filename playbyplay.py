from nba_api.live.nba.endpoints import playbyplay
import pandas as pd

def getPbP(game_id):
    try:
        pbp_data = playbyplay.PlayByPlay(game_id=game_id).get_dict()
        
        # Check if the 'game' and 'actions' keys exist
        if 'game' not in pbp_data or 'actions' not in pbp_data['game']:
            raise ValueError("Invalid response structure from NBA API.")

        actions = pbp_data['game']['actions']
        return actions

    except Exception as e:
        print(f"Error fetching play-by-play: {e}")
        return []
