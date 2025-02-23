from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FitnessLevels(db.Model):
    __tablename__ = 'fitness_levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    exercises = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    program_duration = db.Column(db.Integer, nullable=False, default=6)
    exercise_type = db.Column(db.String(50), nullable=False)
    rest_period = db.Column(db.Integer, nullable=False, default=60)
    repetitions = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    fitness_level_id = db.Column(db.Integer, db.ForeignKey('fitness_levels.id'), nullable=False)
    fitness_level = db.relationship('FitnessLevels', backref=db.backref('training_sessions', lazy=True))
    week_number = db.Column(db.Integer, nullable=False)  # Added week_number for each session

    @property
    def serialize(self):
        return {
            'id': self.id,
            'session_name': self.session_name,
            'duration': self.duration,
            'exercises': self.exercises,
            'notes': self.notes,
            'program_duration': self.program_duration,
            'exercise_type': self.exercise_type,
            'rest_period': self.rest_period,
            'repetitions': self.repetitions,
            'sets': self.sets,
            'fitness_level': self.fitness_level.name,
            'week_number': self.week_number  # Including the week_number
        }
