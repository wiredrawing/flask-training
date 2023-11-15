from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, Date, String, DateTime, func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from lib.setting import engine, base, session
from models.Participant import Participant
from app import login


@login.user_loader
def load_user(id):
    return session.query(User).get(int(id))


# flask-login用に多重継承
class User(UserMixin, base):
    """
    モデルのマイグレーション方法
    (1).
    最新バージョンへのマイグレーション
    alembic upgrade head
    (2).
    マイグレーションを1つ戻す
    alembic downgrade -1
    (3).
    マイグレーションを1つ進める
    alembic upgrade +1
    (4).
    マイグレーションを指定したバージョンまで戻す
    alembic downgrade 123456789
    (5).
    マイグレーションを指定したバージョンまで進める
    alembic upgrade 123456789
    (6).
    マイグレーションを最初まで戻す
    alembic downgrade base
    """
    __tablename__ = 'users'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "ユーザーモデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ユーザーID")
    # emailはユニークとする
    email = Column(String(256), nullable=False, comment="メールアドレス", unique=True)
    password = Column(Text(), nullable=False, comment="パスワード");
    username = Column(Text(), nullable=False, comment="ユーザー名")
    gender = Column(Integer, nullable=False, comment="性別")

    created_at = Column(DateTime, default=func.now(), nullable=False, comment="ユーザー登録日時")
    updated_at = Column(DateTime, default=func.now(), nullable=True, comment="ユーザー更新日時")
    deleted_at = Column(DateTime, default=func.now(), nullable=True, comment="ユーザー削除日時")
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
    # メッセージは最新の投稿順に取得する
    messages = relationship("Message", order_by="Message.id.desc()", backref="user")
    # id asc順に取得
    # messages = relationship("Message", order_by="Message.id.asc()", backref="user")


# Do hash password.
def set_password(self, password):
    self.password_hash = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.password_hash, password)


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
