from flask import Flask, render_template, jsonify
from models import FitnessLevels, TrainingSession, db
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def create_app ( ) :
    app = Flask(__name__)

    # Configure the MySQL URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Qonda_123456@localhost:3307/my_database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Check if the database exists, and create it if necessary
    try :
        # Establish connection to MySQL server
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with engine.connect() as connection :
            # Try creating the database
            connection.execute(f"CREATE DATABASE IF NOT EXISTS my_database")
    except OperationalError as e :
        print(f"Error creating database: {e}")

    return app


# Initialize the app
app = create_app()

# Initialize the database
with app.app_context() :
    db.create_all()


@app.route('/')
def home ( ) :
    greeting = "Are You interested in your journey?"
    return render_template('index.html', greeting=greeting)


@app.route('/api/fitness_levels', methods=['GET'])
def get_fitness_levels ( ) :
    results = db.session.query(FitnessLevels).all()
    return jsonify([level.serialize for level in results])


@app.route('/api/training_sessions/<string:fitness_level>', methods=['GET'])
def get_training_sessions_by_level (fitness_level) :
    fitness_level_record = FitnessLevels.query.filter_by(name=fitness_level).first()

    if not fitness_level_record :
        return jsonify({'error' : 'Invalid fitness level'}), 400

    sessions = db.session.query(TrainingSession).filter(
        TrainingSession.fitness_level_id == fitness_level_record.id).all()

    return jsonify([session.serialize for session in sessions])


if __name__ == "__main__" :
    app.run(host='0.0.0.0', port=5000)
