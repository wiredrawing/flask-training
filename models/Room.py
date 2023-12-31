from datetime import datetime

from sqlalchemy import Column, Integer, Text, Date, String, DateTime, func
from sqlalchemy.orm import relationship, backref

from lib.setting import session, base, engine
from models.Participant import Participant


class Room(base):
    __tablename__ = 'rooms'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "ルームモデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ルームID")
    room_name = Column(String(256), nullable=False, comment="ルーム名")
    description = Column(Text(), nullable=False, comment="ルームの説明")

    created_at = Column(DateTime, nullable=False, comment="作成日時", default=func.now())
    updated_at = Column(DateTime, nullable=True, comment="更新日時※メッセージが投稿されるたびアップデートする", default=func.now())
    deleted_at = Column(DateTime, nullable=True, comment="削除日時", default=func.now())

    # メッセージを最新の投稿順に取得する
    messages = relationship("Message", order_by="Message.id.desc()", back_populates="room")
    participants = relationship("Participant", back_populates="room")


if __name__ == "__main__":
    # デーブルの作成処理
    base.metadata.create_all(engine)
