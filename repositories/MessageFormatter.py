from injector import inject

from interfaces.MessageFormatterInterface import MessageFormatterInterface
from models.Message import Message


# インターフェースを継承する
class MessageFormatter(MessageFormatterInterface):
    """
    MessageFormatter is a class that formats messages for the user.
    """
    def __init__(self, message: Message):
        print("===================>", message)
        self.__message = message

    def to_dict(self):
        print(self.__message)
        print(self.__message.user)
        if self.__message.user is not None and self.__message.room is not None:
            return {
                "id": self.__message.id,
                "message": self.__message.message,
                "room": {
                    "id": self.__message.room_id,
                    "room_name": self.__message.room.room_name,
                    "user_id": self.__message.user_id,
                },
                "user": {
                    "id": self.__message.user_id,
                    "username": self.__message.user.username,
                    "email": self.__message.user.email,
                }
            }
        else:
            raise Exception("Messageモデルのuserまたはroomが存在しません")
