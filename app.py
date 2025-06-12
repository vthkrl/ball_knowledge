from flask import Flask, render_template, request, jsonify
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_live import getTodayGames, getBoxscore
from nba import comparePlayers, getPlayerImage, leagueStandings, constructPlayerBio
from playbyplay import getPbP
from player_performances import getPlayerPerf, getPlayerGameLog
from league_leaders import getLeagueLeaders
from teams import getTeamStats, getTeamInfo, getTeamRoster, teamColors, getTeamGameLog
from datetime import datetime, timezone
from dateutil import parser
from timezone import convertToLTZ

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        p1 = request.form['player1']
        p2 = request.form['player2']
        stats_type = request.form.get('statsType', 'current')  # Get the stats type from form

        try:
            x = comparePlayers(p1, p2, stats_type)  # You'll need to modify your comparePlayers function
                                                   # to handle both current and career stats
            
            p1_image = x[1][0]
            p2_image = x[1][1]
            
            df = x[0]
            table = df.to_html(classes='table table-striped', border=0)
            
            return render_template('compare.html', 
                                 table=table, 
                                 p1=p1, 
                                 p2=p2, 
                                 p1_image=p1_image, 
                                 p2_image=p2_image,
                                 stats_type=stats_type,
                                 )  # Pass the stats type to template
        
        except Exception as e:
            return render_template('compare.html', error=str(e))
        
    return render_template('compare.html')

@app.route('/standings')
def standings():
    try:
        ls = leagueStandings()

        return render_template('standings.html', east = ls['east'], west = ls['west'])
    except Exception as e:
        return jsonify({'error': e})

@app.route('/live-games')
def live_games():
    try:
        games = getTodayGames()    

        return render_template('live_games.html', games=games)

    except Exception as e:
        return render_template('live_games.html', error="Failed to load live games: " + str(e))
    
@app.route('/update_live_games')
def update_live_games():
    try:
        games = getTodayGames()

        return jsonify(games)
    except Exception as e:
        return jsonify({'error': e})

@app.route('/boxscore/<game_id>')
def display_boxscore(game_id):
    boxscore_data = getBoxscore(game_id)

    # Ensure boxscore_data is valid
    if not boxscore_data or 'gameStarted' not in boxscore_data:
        return "Error: Game data unavailable", 500

    if boxscore_data['gameStarted']:
        gameTimeLTZ = convertToLTZ(boxscore_data['gameDetails'].get('gameTimeUTC', ''))

        return render_template(
            'boxscore.html',
            gameDetails=boxscore_data['gameDetails'],
            location=boxscore_data['location'],
            homeTeam=boxscore_data['homeTeam'],
            awayTeam=boxscore_data['awayTeam'],
            gameTimeLTZ=gameTimeLTZ
        )
    else:
        return render_template(
            'simple_boxscore.html',
            boxscore_data=boxscore_data
        )


@app.route('/update_boxscore/<game_id>')
def update_boxscore(game_id):
    try:
        boxscore_data = getBoxscore(game_id)
        gameTimeLTZ = convertToLTZ(boxscore_data['gameDetails']['gameTimeUTC'])
        boxscore_data['gameDetails']['gameTimeLTZ'] = gameTimeLTZ.strftime('%Y-%m-%d %H:%M:%S %Z')  # Add localized time to response

        return jsonify(boxscore_data)
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/<game_id>/<p_id>')
def player_boxscore(p_id, game_id):
    try:
        player_box = getPlayerPerf(p_id, game_id)
        player_name = player_box[1]
        gameTimeLTZ = convertToLTZ(player_box[2]['gameTimeUTC'])

        return render_template('player_box.html',
                            stats = player_box[0],
                            p_id = p_id,
                            player_name = player_name,
                            gameTimeLTZ = gameTimeLTZ,
                            gameDetails = player_box[2])
    except Exception as e:
        return jsonify({'error': e})

@app.route('/update_player_box/<game_id>/<p_id>')
def update_player_box(p_id, game_id):
    try:
        player_box = getPlayerPerf(p_id, game_id)

        return jsonify(player_box)
    except Exception as e:
        return jsonify({'error': e})

@app.route('/player_suggestions')
def player_suggestions():
    try:
        query = request.args.get('query', '').lower()
        all_players = [(player['full_name'], player['id']) for player in players.get_players()]
        suggestions = [(player[0], getPlayerImage(int(player[1])), player[1]) for player in all_players if query in player[0].lower()]
        return jsonify(suggestions[:10])
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_play_by_play/<game_id>')
def get_pbp(game_id):
    try:
        pbp_data = getPbP(game_id)
        boxscore = getBoxscore(game_id)
        homeTeamId = boxscore['homeTeam']['teamId']
        awayTeamId = boxscore['awayTeam']['teamId']

        if not pbp_data:
            return jsonify({'error': 'No play-by-play data available'}), 404
        
        return jsonify({'plays': pbp_data, 'homeTeamId': homeTeamId, 'awayTeamId': awayTeamId}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/league-leaders/<category>')
def league_leaders(category):
    try:
        league_leaders = getLeagueLeaders(category)

        return render_template('league_leaders.html',
                               league_leaders = league_leaders,
                               category = category)
    except Exception as e:
        return jsonify({'error': e})
    
@app.route('/team-stats/<team_id>')
def team_stats(team_id):
    try:
        teamStats = getTeamStats(team_id)
        teamCommonInfo = getTeamInfo(team_id)

        return render_template('team_stats.html',
                               teamStats = teamStats,
                               teamCommonInfo = teamCommonInfo)
    except Exception as e:
        return jsonify({'error': e})

@app.route('/roster/<team_id>')
def get_roster(team_id):
    try:
        x = getTeamRoster(team_id)
        teamRoster = x['teamRoster']
        headCoach = x['headCoach']

        return jsonify({'teamRoster': teamRoster, 'headCoach': headCoach})
    except Exception as e:
        return jsonify({'error': e})
    
@app.route('/player_stats/<p_id>')
def get_player_stats(p_id):
    try:
        player = constructPlayerBio(p_id)
        common_info = player['info']
        stats = player['stats']

        return render_template('player_stats.html',
                               common_info=common_info,
                               stats=stats)
    except Exception as e:
        return jsonify({'error': e})
    
@app.route('/team_colors/<team_id>')
def get_team_colors(team_id):
    try:
        team_colors = teamColors(team_id)

        return jsonify({'team_id': team_id, 'abb': team_colors['abb'], 'colors': team_colors['colors']})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/player_game_log/<p_id>')
def player_game_log(p_id):
    try:
        game_log = getPlayerGameLog(p_id)

        return jsonify(game_log)
    except Exception as e:
        return jsonify({'error': e})

@app.route('/team_game_log/<team_id>')
def team_game_log(team_id):
    try:
        game_log = getTeamGameLog(team_id)

        return jsonify(game_log)
    except Exception as e:
        return jsonify({'error': e})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)