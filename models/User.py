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

    """
        User 1: N Participant
        User has many Participant
        backrefを使うとParticipantから<user>というプロパティ名でUserを参照できるようになる
        user = session.query(User).filter(User.id == 1000).first()
        とあった場合
        user.participants でUserが参加しているParticipantの一覧が取得できる
        逆に
        participant = session.query(Participant).filter(Participant.id == 1000).first()
        この場合は
        participant.user でParticipantのUserを取得できる
    """
    participants = relationship("Participant", backref="user")

    # 対象レコードのユーザーが発言したメッセージ一覧を取得する
    messages = relationship("Message", backref="user")


if __name__ == "__main__":
    """
    alembicコマンド 
    まずモデル等を何かしら変更したら以下のコマンドをうつ
    >> alembic revision --autogenerate -m "create tables"
    とりあえずDBの中身が消えて良いならマイグレーション履歴を呼び出す
    >> alembic history 
    >> alembic upgrade base でマイグレーションを実行する
    >> alembic downgrade base で初期状態へもどす
    """
    base.metadata.create_all(engine)
    users = session.query(User.username).all()
    for user in users:
        print(user.username)
        pass
