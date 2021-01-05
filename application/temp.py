from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.app_context().push()
    return app
app = create_app()