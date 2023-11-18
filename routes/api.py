from json import dumps

import redis
from flask import Flask, Blueprint, render_template, redirect, request, jsonify, make_response

from lib.logger import get_app_logger
from lib.redis_cli import execute_redis
from lib.setting import session
from models.Message import Message
from routes.CreateMessageForm import CreateMessageForm

app = Blueprint('api', __name__, url_prefix='/api')


@app.route("/message/<int:room_id>/create", methods=['POST'])
def create_message(room_id):
    """
    HTTPリクエスト経由でメッセージを登録する
    :param room_id:
    :return:
    """
    try:
        # logger = get_app_logger()
        # リクエストHTTPヘッダーをロギングする
        headers = request.headers;
        print(dir(request))
        print(headers)
        # logger.info(headers)
        """redisクライアントを作成"""
        redis_cli: redis.Redis = execute_redis()

        """postデータを変数化"""
        form = CreateMessageForm(request.form)
        if form.validate() is not True:
            errors = form.errors
            # errors will return.
            return jsonify(errors)

        message = Message(
            message=form.data.get("message"),
            room_id=form.data.get("room_id"),
            user_id=form.data.get("user_id"),
        )
        session.add(message)
        session.commit()
        latest_message_id = message.id

        message = session.query(Message).filter(Message.id == latest_message_id).first()
        if message is None:
            raise Exception("メッセージが登録できませんでした")

        # メッセージをJSON形式に変換する
        print(dir(message))
        json_to_redis = {
            "id": message.id,
            "message": message.message,
            "room_id": message.room_id,
            "room_name": message.room.room_name,
            "user_id": message.user_id,
            "username": message.user.username,
            "email": message.user.email,
        }
        redis_cli.publish("room_id:{}".format(room_id), dumps(json_to_redis))
        # 作成したリソースをJSONで返却する
        response = make_response(json_to_redis, 201)
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response
    except Exception as e:
        print(e)
        errors = {
            "message": "エラーが発生しました"
        }
        errorsJson = dumps(errors)
        # 作成したリソースをJSONで返却する
        response = make_response(errorsJson, 500)
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response


@app.route("/message/<int:room_id>/old/", methods=['POST'])
def old_messages(room_id):
    pass
