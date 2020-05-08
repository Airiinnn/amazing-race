from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email):
        self.id = id_
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2]
        )
        return user

    @staticmethod
    def create(id_, name, email):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email) "
            "VALUES (?, ?, ?)",
            (id_, name, email),
        )
        db.commit()
