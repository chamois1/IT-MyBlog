from flask import Flask, session
from flask_session import Session
from flask_ckeditor import CKEditor
from flask_migrate import Migrate

from db import db_init, db
from models import Accounts_Users
from flask_bcrypt import Bcrypt

# routes
from routes.admin_panel import admin_bp
from routes.posts_routes import posts_bp
from routes.profile_users import profiles
from routes.main_routes import main_routes


def create_app(database_uri="postgresql://username:password@localhost:5432/blog"):
    # settings
    app = Flask(__name__)
    ckeditor = CKEditor(app)

    # urls from file admin_panel
    app.register_blueprint(main_routes)
    app.register_blueprint(profiles)
    app.register_blueprint(admin_bp)
    app.register_blueprint(posts_bp)

    # config
    app.config['SECRET_KEY'] = '(#U(@FU*AUF*UIAJ091E)!(@#$*190()$!2497() FUIAJQIJ*($@#!*7EDSAIJIDJAS)))'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/images/'

    db_init(app)
    Session(app)
    
    """
    Added for convenience when working with models
    0. Create new column in models
    1. flask db init
    2. flask db migrate -m "Initial Migration"
    3. flask db upgrade
    Done! Model upgraded.
    """
    migrate = Migrate(app, db)  


    # function will pass variables for all html
    @app.context_processor
    def session_base():
        session_is_admin = session.get('is_admin')
        id_session = session.get('id')
        return dict(session_is_admin=session_is_admin, id_session=id_session)

    return app


app = create_app()

"""
Creating hard account for admin
If you wish, you can delete or change the data
"""

with app.app_context():
    
    # Create hard account
    def create_hardcoded_account_admin():

        password = 'admin12345'.encode('utf-8')
        bcrypt = Bcrypt()
        data_admin = [
            {'login': 'admin', 'email': 'admin@admin.com', 'password': bcrypt.generate_password_hash(password), 'is_admin': True},
        ]
        
        for entry in data_admin:
            if not Accounts_Users.query.filter_by(email=entry['email']).first():
                admin = Accounts_Users(login=entry['login'], email=entry['email'], password=entry['password'], is_admin=entry['is_admin'])
                db.session.add(admin)

        db.session.commit()
        db.session.close()

    create_hardcoded_account_admin()


if __name__ == '__main__':
    app.run(debug=True)
