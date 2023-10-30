from sqlalchemy import Column, Integer, Text

from lib.setting import session, base, engine


class Room(base):
    __tablename__ = 'rooms'
    __table_args__ = {
        'mysql_collate': 'utf8_general_ci',
        "comment": "ルームモデル",
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ルームID")
    room_name = Column(Text(), nullable=False, comment="ルーム名")
    description = Column(Text(), nullable=False, comment="ルームの説明")


if __name__ == "__main__":
    # デーブルの作成処理
    base.metadata.create_all(engine)
