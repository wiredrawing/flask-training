from sqlalchemy import Column, Integer, Text
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
    messages = relationship("Message", backref=backref("room"))
    # messages = relationship("Message", backref="room", secondary=Message.__table__, order_by=Message.id.desc())


if __name__ == "__main__":
    # デーブルの作成処理
    base.metadata.create_all(engine)
