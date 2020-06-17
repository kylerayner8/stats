from flask import (
    Blueprint, flash, g ,redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from wispr.db import get_db

bp = Blueprint('stats', __name__)

def get_all_players():
    players = get_db().execute(
        'SELECT id, player_name FROM stats'
    ).fetchall()
    for player in players:
        print(player.keys())
    return players


@bp.route('/')
def index():
    player_list = get_all_players()
    print(player_list)
    return render_template('/stats/index.html', player_list=player_list)


@bp.route('/data/<int:id>')
def data(id):
    row = get_db().execute(
        'SELECT id, player_name, points, rebounds, points_per_game FROM stats WHERE id = ?', (id,)
    ).fetchone()
    get_all_players()
    data = {
        "name": row['player_name'],
        "points": row['points'],
        "points_per_game": row['points_per_game']
    }
    return render_template('/stats/display.html', data=[data])


@bp.route('/search', methods=['POST'])
def search():
    print(request.form)
    player_index = request.form['option']
    print(player_index)
    return redirect(url_for('stats.data', id=player_index))