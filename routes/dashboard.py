from flask import Flask, Blueprint, session as http_session, render_template, request, redirect
from lib.setting import session, engine
from models.User import User

app = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@app.route("/", methods=['GET'])
def dashboard():
    if "user_id" in http_session:
        print("=====================================")
    user_id = http_session["user_id"]
    user = session.query(User).filter(User.id == user_id).first()
    print("==================");
    return render_template("dashboard/dashboard.html", user=user)


@app.route("/edit", methods=['GET'])
def edit():
    """"現在ログインしているユーザーの情報を表示"""
    if "user_id" in http_session:
        user = session.query(User).filter(User.id == http_session["user_id"]).first()
        return render_template("dashboard/edit.html", user=user)
    else:
        return "ログインしてください"


@app.route("/update", methods=['POST'])
def update():
    required_key = [
        "id",
        "email",
        "username",
    ]
    if "user_id" in http_session:
        post_data = request.form.to_dict()
        if required_key == list(post_data.keys()):
            user = session.query(User).filter(User.id == http_session["user_id"]).first()
            user.email = post_data["email"]
            user.username = post_data["username"]
            session.commit()
            return redirect("/dashboard/edit")
    else:
        return "ログインしてください"