import json
from datetime import datetime
from time import sleep

import redis
from flask import Blueprint, render_template, request, redirect, session as http_session, make_response

from lib.redis_cli import execute_redis
from lib.setting import session
from models.Message import Message

app = Blueprint('server_sent_event', __name__, url_prefix='/sse')


@app.route("/messages/<int:room_id>/", methods=['GET'])
def messages_on_room(room_id):
    __now = datetime.now();
    current_time = __now.strftime("%Y-%m-%d %H:%M:%S")

    # リアルタイムのメッセージはredis-serverから取得する
    # 古いデータはDBから取得する
    r: redis.Redis = execute_redis()

    response = make_response(_fetch_message(room_id, current_time, r))
    response.headers['Content-Type'] = 'text/event-stream; charset=UTF-8'
    return response


def _fetch_message(room_id, current_time, r):
    """
    メッセージを取得する
    :param room_id: integer
    :param current_time: datetime.datetime
    :param r: redis.Re
    :return:
    """
    p = r.pubsub()
    redis_key = "room_id:{}".format(room_id)
    p.subscribe(redis_key)

    for item in p.listen():
        print("redis-serverからデータを取得")
        print(item)
        if item["type"] == "message":
            message = item["data"].decode("utf-8")
            message_obj = {
                "message": message,
                "user_id": 0,
                "username": "redis-server",
            }
            # メッセージをJSON形式に変換する
            data = "data: {}\n\n".format(json.dumps(message_obj))
            print(data)
            yield data
        else:
            print("redis-serverからデータを取得できませんでした")
            print(item)
            # break
    # latest_id = 0
    # while True:
    #     # 指定したroom_idのアクセス時点より最新のメッセージを取得する
    #     if latest_id == 0:
    #         messages = session.query(Message).filter(
    #             Message.room_id == room_id,
    #             Message.created_at >= current_time,
    #         ).all()
    #     else:
    #         messages = session.query(Message).filter(
    #             Message.room_id == room_id,
    #             Message.id > latest_id,
    #         ).all()
    #     print(messages)
    #     if len(messages) > 0:
    #         print("メッセージを取得-------------");
    #     for message in messages:
    #         message_obj = {
    #             "message": message.message,
    #             "user_id": message.user_id,
    #             "username": message.user.username,
    #         }
    #         # メッセージをJSON形式に変換する
    #         data = "data: {}\n\n".format(json.dumps(message_obj))
    #         # data = "data: {}\n\n".format(message.message)
    #         print(data)
    #         latest_id = message.id
    #         yield data
    #     session.commit()
    #     print("server sent event ----------------")
    #     print(current_time)
    #     sleep(1)
