from flask import Flask
from flask_login import LoginManager


app = Flask(__name__, template_folder="templates")

login = LoginManager(app)



# alembic のマイグレーション方法
# > alembic init <プロジェクトの名前>
