from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from lib.setting import engine, base, session
from models.Participant import Participant

class User(base):
    __tablename__ = 'users'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "ユーザーモデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ユーザーID")
    email = Column(Text(), nullable=False, comment="メールアドレス")
    password = Column(Text(), nullable=False, comment="パスワード");
    username = Column(Text(), nullable=False, comment="ユーザー名")
    gender = Column(Integer, nullable=False, comment="性別")

    participants = relationship("Participant", backref="participants")


if __name__ == "__main__":
    base.metadata.create_all(engine)
    users = session.query(User.username).all()
    for user in users:
        print(user.username)
        pass
