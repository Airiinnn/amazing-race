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
        
        # DELETE THIS AFTER MANUALLY SETTING PASSWORDS
        db.execute(
            "INSERT INTO progress (email, mainstage, psw) "
            "VALUES (?, 0, '-')",
            (email,),
        )

        db.execute(
            "INSERT INTO stage0 (email, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20) "
            "VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)",
            (email,),
        )

        db.execute(
            "INSERT INTO stage1 (email, q1, q2, q3, q4) "
            "VALUES (?, 0, 0, 0, 0)",
            (email,),
        )

        db.execute(
            "INSERT INTO stage2 (email, q1, q2, q3, q4, q5, q6, q7, q8) "
            "VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0)",
            (email,),
        )

        db.execute(
            "INSERT INTO stage3 (email, q1, q2, q3) "
            "VALUES (?, 0, 0, 0)",
            (email,),
        )

        db.execute(
            "INSERT INTO stage7 (email, q1, q2, q3, q4, q5, q6) "
            "VALUES (?, 0, 0, 0, 0, 0, 0)",
            (email,),
        )
        db.commit()
