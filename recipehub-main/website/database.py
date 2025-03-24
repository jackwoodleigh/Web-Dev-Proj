from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def check_users():
    from website import create_app
    from website.models import User
    app = create_app()
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"User ID: {user.id}, Email: {user.email}")