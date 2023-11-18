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
    :param r: redis.Redis
    :return:
    """
    p = r.pubsub()
    redis_key = "room_id:{}".format(room_id)
    p.subscribe(redis_key)

    for item in p.listen():
        if item["type"] == "message":
            message = item["data"].decode("utf-8")
            # decorded_message = json.loads(message)
            # メッセージをJSON形式に変換する
            data_list = [
                "event: new-message",
                "data: {}".format(message),
                "retry: 1000",
                "\n"]
            data = "\n".join(data_list)
            yield data
        else:
            print("redis-serverからデータを取得できませんでした")
            print(item)
