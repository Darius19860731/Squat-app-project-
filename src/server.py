from flask import Flask, jsonify, render_template

from models import db, FitnessLevels

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Qonda_123456@mysql-container:3306/my_database'

# replace this with your database URI

db.init_app(app)


@app.route('/api/training_sessions/<level>', methods=['GET'])
def get_training_sessions (level) :
    # First, we find the fitness level by its name.
    fitness_level = FitnessLevels.query.filter(FitnessLevels.name == level).first()

    if not fitness_level :
        return jsonify({"error" : f"No such fitness level as {level}"}), 404

    # Now we get the training sessions for that fitness level, and serialize them to make them JSON serializable.
    training_sessions = [session.serialize for session in fitness_level.training_sessions]

    # And finally, we return these as a JSON response.
    return jsonify(training_sessions)

