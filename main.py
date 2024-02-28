import os
import csv
import time
import json
from random import randrange, uniform

from flask import Flask, request, render_template, jsonify

from harness_featureflags import FeatureFlagClient
from logger_config import setup_logger
from metrics_config import CACHE_HITS, CACHE_MISSES, REQUEST_DURATION, HITS
from database import Session, SoccerTeam, engine, Base
from cache import cache_data, get_cached_data, get_redis_object
import json
from dotenv import load_dotenv
from prometheus_client import make_wsgi_app, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from threading import Thread

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger()

# Define a Histogram for tracking latencies with labels for cache and db
LATENCY = Histogram('service_latency_seconds', 'Service latency in seconds', ['type'])

app = Flask(__name__)
ff_client = FeatureFlagClient()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    start_time = time.time()
    query = request.form['query']
    cached_result = get_cached_data(query)

    demo_json = ff_client.get_demo_variation()
    logger.info("Type of demo_json: {0}".format(type(demo_json)))

    if cached_result:
        latency = time.time() - start_time
        CACHE_HITS.inc()
        HITS.labels(type='cache').inc()
        LATENCY.labels(type='cache').observe(latency)
        logger.info(f"Cache hit for query '{query}'. Latency: {latency:.3f} seconds.")
        return jsonify(data=json.loads(cached_result.decode('utf-8')), source='cache')
    else:
        session = Session()
        result = session.query(SoccerTeam).filter(SoccerTeam.name.contains(query)).all()

        range_min = float(demo_json['min'])
        range_max = float(demo_json['max'])
        logger.info(f"Demo range: {range_min} - {range_max}")
        random_demo_range = uniform(range_min, range_max)
        time.sleep(random_demo_range)

        latency = time.time() - start_time
        HITS.labels(type='db').inc()
        CACHE_MISSES.inc()
        LATENCY.labels(type='db').observe(latency)
        logger.info(f"Cache miss for query '{query}'. DB query latency: {latency:.3f} seconds.")
        result_json = [{'name': team.name, 'country': team.country, 'city': team.city,
                        'foundation': team.foundation, 'stadium': team.stadium}
                       for team in result]
        cache_data(query, json.dumps(result_json))
        session.close()
        REQUEST_DURATION.observe(latency)
        return jsonify(data=result_json, source='db')


# Setup Prometheus metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


@app.route('/wipe_redis', methods=['GET'])
def wipe_redis():
    try:
        r = get_redis_object()
        r.flushdb()  # Assuming 'r' is your Redis connection object
        return jsonify({"success": True, "message": "Redis cache wiped successfully."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/wipe_postgres', methods=['GET'])
def wipe_postgres():
    try:
        # Assuming SoccerTeam is your SQLAlchemy model for the soccer_teams table
        SoccerTeam.__table__.drop(engine)
        SoccerTeam.__table__.create(engine)
        return jsonify({"success": True, "message": "Postgres soccer_teams table wiped successfully."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/load_clubs', methods=['GET'])
def load_clubs():
    def async_load_clubs():
        try:
            session = Session()
            with open('data/soccer_teams.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    team = SoccerTeam(
                        name=row['name'],
                        country=row['country'],
                        city=row['city'],
                        foundation=row['foundation'],
                        stadium=row['stadium']
                    )
                    session.add(team)
                session.commit()
            print("Clubs loaded into Postgres successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error loading clubs: {e}")
        finally:
            session.close()

    # Start the loading process in a background thread
    thread = Thread(target=async_load_clubs)
    thread.start()

    # Immediately return a response to the client
    return jsonify({"message": "Loading clubs in the background"}), 202


if __name__ == "__main__":
    DATABASE_URL = os.getenv("GABS_DATABASE_URL")
    REDIS_URL = os.getenv("GABS_REDIS_URL")
    print("DATABASE URL MAIN: {0}".format(DATABASE_URL))
    print("REDIS URL MAIN: {0}".format(REDIS_URL))
    app.run(host='0.0.0.0', port=5000, debug=True)
