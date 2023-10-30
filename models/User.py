from sqlalchemy import Column, Integer, Text
from lib.setting import engine, base, session


class User(base):
    __tablename__ = 'users'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "ユーザーモデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ユーザーID")
    username = Column(Text(), nullable=False, comment="ユーザー名")
    gender = Column(Integer, nullable=False, comment="性別")


if __name__ == "__main__":
    base.metadata.create_all(engine)
    users = session.query(User.username).all()
    for user in users:
        print(user.username)
        pass
