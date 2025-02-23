from app import create_app
from models import db, FitnessLevels, TrainingSession
from sqlalchemy.exc import SQLAlchemyError

app = create_app()

with app.app_context() :
    try :
        # Create tables if they don't exist
        db.create_all()

        # Seed fitness levels
        levels = [
            {"name" : "Beginner", "description" : "Start your journey here!"},
            {"name" : "Intermediate", "description" : "Step it up!"},
            {"name" : "Elite", "description" : "Advanced training for serious athletes."},
            {"name" : "Master", "description" : "Challenge yourself to the max."},
            {"name" : "Grand Master", "description" : "For the best of the best."},
        ]

        for level in levels :
            existing_level = FitnessLevels.query.filter_by(name=level['name']).first()
            if not existing_level :
                fitness_level = FitnessLevels(name=level['name'], description=level['description'])
                db.session.add(fitness_level)

        db.session.commit()  # Commit fitness levels first

        # Fetch all fitness levels and verify they exist
        level_dict = {level.name : level for level in FitnessLevels.query.all()}
        print("Fitness Levels in DB:", list(level_dict.keys()))  # Debugging output

        # Validate that all levels exist
        missing_levels = [lvl["name"] for lvl in levels if lvl["name"] not in level_dict]
        if missing_levels :
            print(f"Error: Missing fitness levels {missing_levels}")
            exit()

        # Training sessions data
        sessions = [
            {"session_name" : "Beginner Session 1", "duration" : 30, "exercises" : "Push-ups, Squats",
             "exercise_type" : "Strength", "sets" : 3, "repetitions" : 10,
             "fitness_level_id" : level_dict["Beginner"].id, "week_number" : 1},

            {"session_name" : "Beginner Session 2", "duration" : 30, "exercises" : "Lunges, Plank",
             "exercise_type" : "Strength", "sets" : 3, "repetitions" : 12,
             "fitness_level_id" : level_dict["Beginner"].id, "week_number" : 2},

            {"session_name" : "Intermediate Session 1", "duration" : 40, "exercises" : "Pull-ups, Deadlifts",
             "exercise_type" : "Strength", "sets" : 4, "repetitions" : 8,
             "fitness_level_id" : level_dict["Intermediate"].id, "week_number" : 1},

            {"session_name" : "Elite Session 1", "duration" : 45, "exercises" : "Bench Press, Squat Jumps",
             "exercise_type" : "Strength", "sets" : 5, "repetitions" : 6, "fitness_level_id" : level_dict["Elite"].id,
             "week_number" : 1},

            {"session_name" : "Master Session 1", "duration" : 50, "exercises" : "Olympic Lifts, Sprints",
             "exercise_type" : "Strength", "sets" : 5, "repetitions" : 5, "fitness_level_id" : level_dict["Master"].id,
             "week_number" : 1},

            {"session_name" : "Grand Master Session 1", "duration" : 60, "exercises" : "Ironman Training, Power Cleans",
             "exercise_type" : "Endurance", "sets" : 6, "repetitions" : 4,
             "fitness_level_id" : level_dict["Grand Master"].id, "week_number" : 1},
        ]

        for session in sessions :
            existing_session = TrainingSession.query.filter_by(session_name=session['session_name']).first()
            if not existing_session :
                training_session = TrainingSession(
                    session_name=session['session_name'],
                    duration=session['duration'],
                    exercises=session['exercises'],
                    exercise_type=session['exercise_type'],
                    sets=session['sets'],
                    repetitions=session['repetitions'],
                    fitness_level_id=session['fitness_level_id'],
                    week_number=session['week_number']
                )
                db.session.add(training_session)

        # Commit all changes
        db.session.commit()
        print("Database seeding complete!")

    except SQLAlchemyError as e :
        db.session.rollback()
        print(f"An error occurred while seeding the database: {str(e)}")
    finally :
        db.session.remove()
