import json
from datetime import datetime
from time import sleep

from flask import Blueprint, render_template, request, redirect, session as http_session, make_response

from lib.setting import session
from models.Message import Message

app = Blueprint('server_sent_event', __name__, url_prefix='/sse')


@app.route("/messages/<int:room_id>/", methods=['GET'])
def messages_on_room(room_id):
    __now = datetime.now();
    current_time = __now.strftime("%Y-%m-%d %H:%M:%S")
    response = make_response(_fetch_message(room_id, current_time))
    response.headers['Content-Type'] = 'text/event-stream; charset=UTF-8'
    return response


def _fetch_message(room_id, current_time):

    latest_id = 0
    while True:
        # 指定したroom_idのアクセス時点より最新のメッセージを取得する
        if latest_id == 0:
            messages = session.query(Message).filter(
                Message.room_id == room_id,
                Message.created_at > current_time,
            ).all()
        else :
            messages = session.query(Message).filter(
                Message.room_id == room_id,
                Message.id > latest_id,
            ).all()
        print(messages)
        for message in messages:
            message_obj = {
                "message": message.message,
                "user_id": message.user_id,
                "username": message.user.username,
            }
            # メッセージをJSON形式に変換する
            data = "data: {}\n\n".format(json.dumps(message_obj))
            # data = "data: {}\n\n".format(message.message)
            print(data)
            latest_id = message.id
            yield data
        session.commit()
        print("server sent event ----------------")
        print(current_time)
        sleep(1)