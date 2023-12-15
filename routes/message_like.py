# from flask import Blueprint, render_template, request, redirect, url_for,make_response, jsonify
#
# from lib.setting import session
# from models.MessageLike import MessageLike
# from routes.CreateNewLikeForm import CreateNewLikeForm, get_create_new_like_schema
#
# app = Blueprint('message_like', __name__, url_prefix='/message')
#
#
# # 指定したメッセージにいいねをする
# @app.route("/<int:message_id>/like", methods=['POST'])
# def like(message_id):
#     schema = get_create_new_like_schema(request.json)
#     # form = CreateNewLikeForm(request.form)
#
#     if form.validate() is not True:
#         print("いいねフォーム------->", form.errors);
#
#     try:
#         print(dir(form))
#         print(form.data)
#         validated_data = form.data
#         message_like = MessageLike(**validated_data)
#         session.add(message_like)
#         session.commit()
#         print(message_like)
#         print(message_like.id)
#         print(message_like.user.id);
#         print(message_like.message.id)
#         pass
#     except Exception as e:
#         print(e)
#
#     return ""
