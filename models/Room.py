from sqlalchemy import Column, Integer, Text, Date
from sqlalchemy.orm import relationship, backref

from lib.setting import session, base, engine
from models.Message import Message


class Room(base):
    __tablename__ = 'rooms'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "ルームモデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ルームID")
    room_name = Column(Text(), nullable=False, comment="ルーム名")
    description = Column(Text(), nullable=False, comment="ルームの説明")
    created_at = Column(Date, nullable=True, comment="作成日時")
    updated_at = Column(Date, nullable=True, comment="更新日時※メッセージが投稿されるたびアップデートする")
    deleted_at = Column(Date, nullable=True, comment="削除日時")

    # メッセージを最新の投稿順に取得する
    messages = relationship("Message", order_by="Message.id.desc()", backref=backref("room"))



if __name__ == "__main__":
    # デーブルの作成処理
    base.metadata.create_all(engine)
