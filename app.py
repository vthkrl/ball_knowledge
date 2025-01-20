from flask import Flask, render_template, request
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba import comparePlayers

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def compare():
    if request.method == 'POST':
        p1 = request.form['player1']
        p2 = request.form['player2']

        x = comparePlayers(p1, p2)

        p1_image = x[1][0]
        p2_image = x[1][1]

        try:
            df = x[0]
            table = df.to_html(classes='table table-striped', border = 0)
            return render_template('compare.html', table = table, p1= p1, p2= p2, p1_image = p1_image, p2_image = p2_image)
        
        except Exception as e:
            return render_template('compare.html', error = str(e))
        
    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug = True)
