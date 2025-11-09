from flask import Flask,session
from . import db
from . import auth
from . import main
from . import recruiter
from . import admin

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', # Change this in a real environment
        DATABASE=db.DATABASE,
    )

    # Initialize DB (run once on startup)
    db.init_db(app)

    # Register app context teardown functions
    app.teardown_appcontext(db.close_connection)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(recruiter.bp)
    app.register_blueprint(admin.bp)
    
    # Make '/' the main entry point for the 'main' blueprint
    app.add_url_rule('/', endpoint='main.home') 

    # Inject session data into all templates for dynamic nav bar
    @app.context_processor
    def inject_user_data():
        return dict(
            logged_in='user_id' in session,
            username=session.get('username'),
            role=session.get('user_role')
        )

    return app