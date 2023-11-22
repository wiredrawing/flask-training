import time
from abc import ABC
from json import dumps

import redis
from flask import Flask, Blueprint, render_template, redirect, request, jsonify, make_response
from injector import inject, Injector

from interfaces.MessageFormatterInterface import MessageFormatterInterface
from lib.logger import get_app_logger
from lib.redis_cli import execute_redis
from lib.setting import session, MAX_POOL_SIZE
from models.Message import Message
from repositories.MessageFormatter import MessageFormatter
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
        # print(dir(request))
        # print(headers)
        # logger.info(headers)
        """redisクライアントを作成"""
        redis_cli: redis.Redis = execute_redis()

        """postデータを変数化"""
        form = CreateMessageForm(request.form)
        if form.validate() is not True:
            errors = form.errors
            # errors will return.
            return jsonify(errors)

        # 現在のコネクション数を取得する
        sql = """
        select * from information_schema.processlist where db = 'flask-test' and command = 'Query';
        """

        result = session.execute(sql);
        all_connections = result.fetchall()
        # print(all_connections);
        current_connections_number = len(all_connections)
        print("<<This is connections number. {}>>".format(current_connections_number))
        # 実行中のコネクション数が一定数を超えた場合はエラーを返却する
        # 現在の既定値は15とする
        if current_connections_number > MAX_POOL_SIZE:
            raise Exception("現在のコネクション数が多すぎます。しばらく時間をおいてから再度お試しください。")
        for row in all_connections:
            print(row)
        try:
            message = Message(
                message=form.data.get("message"),
                room_id=form.data.get("room_id"),
                user_id=form.data.get("user_id"),
            )
            session.add(message)
            # raise Exception("Failed commit");
            session.commit()
        except Exception as e:
            session.rollback()
            get_app_logger().error(e)
            raise Exception("メッセージの登録に失敗しました")
        latest_message_id = message.id
        print("********************", latest_message_id, "##########################")

        # message = session.query(Message).filter(Message.id == latest_message_id).first()
        # if message is None:
        #     raise Exception("メッセージが登録できませんでした")
        # print("********************", vars(message), "##########################")

        # メッセージを規程のJSON形式に変換させるためにDIコンテナを利用する
        # MessageFormatterはServer Sent Eventのコントローラ側でも利用する
        message_formatter = MessageFormatter(message)
        json_to_redis = message_formatter.to_dict()
        redis_cli.publish("room_id:{}".format(room_id), dumps(json_to_redis))
        # 作成したリソースをJSONで返却する
        response = make_response(json_to_redis, 201)
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response
    except Exception as e:
        print(e)
        get_app_logger().error(e)
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
