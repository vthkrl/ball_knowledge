from flask import Flask, render_template, request, jsonify
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_live import getTodayGames, getBoxscore
from nba import comparePlayers, getPlayerImage
from playbyplay import getPbP
from datetime import datetime, timezone
from dateutil import parser

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

@app.route('/live-games')
def live_games():
    # Sample API URL - Replace with actual NBA live game endpoint
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
    gameTimeLTZ = parser.parse(boxscore_data['gameDetails']['gameTimeUTC']).replace(tzinfo=timezone.utc).astimezone(tz=None)

    return render_template(
        'boxscore.html',
        gameDetails=boxscore_data['gameDetails'],
        location=boxscore_data['location'],
        homeTeam=boxscore_data['homeTeam'],
        awayTeam=boxscore_data['awayTeam'],
        gameTimeLTZ=gameTimeLTZ
    )

@app.route('/update_boxscore/<game_id>')
def update_boxscore(game_id):
    try:
        boxscore_data = getBoxscore(game_id)
        gameTimeLTZ = parser.parse(boxscore_data['gameDetails']['gameTimeUTC']).replace(tzinfo=timezone.utc).astimezone(tz=None)
        boxscore_data['gameDetails']['gameTimeLTZ'] = gameTimeLTZ.strftime('%Y-%m-%d %H:%M:%S %Z')  # Add localized time to response

        return jsonify(boxscore_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/player_suggestions')
def player_suggestions():
    query = request.args.get('query', '').lower()
    print("Received query:", query)  # Debugging line
    all_players = [(player['full_name'], player['id']) for player in players.get_players()]
    suggestions = [(player[0], getPlayerImage(int(player[1]))) for player in all_players if query in player[0].lower()]
    print("Suggestions found:", suggestions[:10])  # Debugging line
    return jsonify(suggestions[:10])

@app.route('/get_play_by_play/<game_id>')
def get_pbp(game_id):
    try:
        pbp_data = getPbP(game_id)

        if not pbp_data:
            return jsonify({'error': 'No play-by-play data available'}), 404
        
        return jsonify({'plays': pbp_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)