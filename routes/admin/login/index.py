from flask import Flask, render_template, request, redirect, url_for, Blueprint, session as http_session, jsonify

# 管理画面向けルーティング
app = Blueprint('admin/login', __name__, url_prefix='/login')


@app.route("/", methods=['GET'])
def index():
    return "管理側ログイン画面です"


@app.route("/", methods=['POST'])
def login():
    """管理ユーザーの実際のログインを処理する"""
    return "管理側ログイン画面です(post)"


@app.route("/any", methods=['GET'])
def any_url():
    return "any"
