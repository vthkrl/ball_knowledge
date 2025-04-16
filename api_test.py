from nba_api.stats.endpoints import commonteamroster, teamplayerdashboard

okc = 1610612760
 
r = commonteamroster.CommonTeamRoster(okc).get_data_frames()[0].columns
d = teamplayerdashboard.TeamPlayerDashboard(okc).get_data_frames()[1]

print(r)
print(d)