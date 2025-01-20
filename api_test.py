from nba_api.stats.endpoints import drafthistory
import json
import pandas as pd

draft = drafthistory.DraftHistory()

print(type(draft.get_json()))
