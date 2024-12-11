from flask import Flask, session
from database.models import init_db
from database.database_utils import delete_all_data, describe_table
from flask_caching import Cache
from routes import games, players, scores
from config import DEBUG
from datetime import timedelta
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=30)


cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
app.config['CACHE'] = cache

init_db()

app.register_blueprint(games.bp)
app.register_blueprint(players.bp)
app.register_blueprint(scores.bp)

if __name__ == "__main__":
    app.run(debug=DEBUG)
