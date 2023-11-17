from json import dumps

import redis
from flask import Flask, Blueprint, render_template, redirect, request, jsonify, make_response

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

        json = dumps(form.data)

        redis_cli.publish("room_id:{}".format(room_id), json)
        # 作成したリソースをJSONで返却する
        response = make_response(json, 201)
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response
    except Exception as e:
        errors = {
            "message": "エラーが発生しました"
        }
        errorsJson = dumps(errors)
        # 作成したリソースをJSONで返却する
        response = make_response(errorsJson, 201)
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response
