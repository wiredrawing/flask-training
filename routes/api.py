import json
from json import dumps
import redis
from flask import Flask, Blueprint, render_template, redirect, request, jsonify, make_response
from flask_login import current_user

from lib.logger import get_app_logger
from lib.redis_cli import execute_redis
from lib.setting import session, MAX_POOL_SIZE
from models.Message import Message
from models.MessageLike import MessageLike
from repositories.MessageFormatter import MessageFormatter
from routes.CreateMessageForm import CreateMessageForm, check_ng_message, check_message_length
from routes.CreateNewLikeForm import get_create_new_like_schema

app = Blueprint('api', __name__, url_prefix='/api')


@app.route("/message/<int:room_id>/create", methods=['POST'])
def create_message(room_id):
    get_app_logger(__name__).info(">>>>>>>>>>>メッセージの登録を開始します")
    """
    HTTPリクエスト経由でメッセージを登録する
    :param room_id:
    :return:
    """
    try:
        """redisクライアントを作成"""
        redis_cli: redis.Redis = execute_redis()

        """postデータを変数化"""
        get_app_logger(__name__).info("test >>>>>>>>>>>メッセージの登録を開始します")
        schema = CreateMessageForm()
        # スキーマにバリデーターを追加する
        schema.fields["message"].validators = [check_ng_message, check_message_length]
        get_app_logger(__name__).info(request.json)
        error_messages: dict = schema.validate(request.json)
        # error_messages: dict = scheme.validate({})
        # エラーメッセージが空っぽでない場合はエラーを返却する
        if error_messages != {}:
            get_app_logger(__name__).error(error_messages)
            return jsonify(error_messages)

        # バリデーション成功時
        validated_data = schema.load(request.json)

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
        # for row in all_connections:
        #     print(row)

        try:
            # session.begin(subtransactions=True)
            message = Message(
                message=validated_data["message"],
                room_id=validated_data["room_id"],
                user_id=validated_data["user_id"],
            )
            session.add(message)
            session.commit()
        except Exception as e:
            session.rollback()
            get_app_logger(__name__).error(e)
            raise Exception("メッセージの登録に失敗しました")
        latest_message_id = message.id
        get_app_logger(__name__).info(">>>>>>>>>>>メッセージの登録が終了しました")
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
        get_app_logger(__name__).error(e)
        errors = {
            "message": "エラーが発生しました"
        }
        errorsJson = dumps(errors)
        # 作成したリソースをJSONで返却する
        response = make_response(errorsJson, 500)
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        return response


# 指定したメッセージに<いいね>をする
@app.route("/message/<int:message_id>/like", methods=['POST'])
def like(message_id):
    """
    指定したメッセージに<いいね>をする
    :param message_id:
    :return:
    """
    # 関数でラップしたスキーマクラスを返却する
    schema_class = get_create_new_like_schema(current_user.id)
    schema = schema_class()
    # schema = CreateNewLikeForm()
    error_messages = schema.validate(request.json)
    if bool(error_messages) is True:
        # バリデーションエラーの場合はエラーを表示
        return jsonify(error_messages)

    # バリデーションが成功した場合はバリデーション結果を取得する
    validated_data = schema.load(request.json)

    # 既にいいねしている場合はその旨を返却する
    exists = session.query(MessageLike).filter(
        MessageLike.user_id == validated_data["user_id"],
        MessageLike.message_id == validated_data["message_id"]
    ).first()

    # いいねが存在しない場合は新規に作成する
    if exists is None:
        message_like = MessageLike(user_id=validated_data["user_id"], message_id=validated_data["message_id"])
        session.add(message_like)
        session.commit()
        get_app_logger(__name__).info("いいねを登録しました")
    else:
        get_app_logger(__name__).info("既にいいねしています")

    max_likes = session.query(MessageLike).filter(MessageLike.message_id == validated_data["message_id"]).count()
    result = {
        "likes": max_likes
    }
    return jsonify(result)


@app.route("/message/<int:room_id>/old/", methods=['POST'])
def old_messages(room_id):
    pass
