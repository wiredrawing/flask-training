# 環境変数 PYTHONPATHに<.>を追加して
# インポートできるようにしておくこと
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import QueuePool

from lib.logger import get_app_logger

try:
    MAX_POOL_SIZE = 15
    MAX_OVERFLOW = 10
    # 接続先DBの設定
    db_user = "root"
    db_pass = "root"
    db_host = "localhost:13306"
    db_name = "flask-test"
    # 接続文字列の作成
    # 参照URL: https://dev.classmethod.jp/articles/sqlalchemy-connection-pooling/
    host_name = "mysql://{}:{}@{}/{}?charset=utf8".format(db_user, db_pass, db_host, db_name)
    engine = create_engine(host_name, echo=False, poolclass=QueuePool, pool_size=MAX_POOL_SIZE, max_overflow=MAX_OVERFLOW)

    # モデルクラスの基底クラスを作成
    base = declarative_base()
    session_factory = sessionmaker(engine)
    session = scoped_session(session_factory)
except Exception as e:
    get_app_logger().error(e)
    # print(e);
    # print("any error happen")

    # alembic の使い方
    """
    >> alembic init <プロジェクト名>
    versionsフォルダが作成される
    alembic.iniの中身を書き換える
    sqlalchemy.url = mysql://<ユーザー名>:<パスワード>@<ホスト名>:<ポート>/<DB名>
    env.pyにアプリケーションで利用するモデルファイルをよみこませる
    >> alembic revision --autogenerate -m "create tables"
    --autogenerate オプションを指定すると、モデルの変更をもとにマイグレーションファイルを自動生成してくれる
    >> alembic upgrade head
    でマイグレーションが実行される
    """
