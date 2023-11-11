# 環境変数 PYTHONPATHに<.>を追加して
# インポートできるようにしておくこと
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
try:

    # 接続先DBの設定
    db_user = "root"
    db_pass = "root"
    db_host = "localhost:13306"
    db_name = "flask-test"
    # 接続文字列の作成
    host_name = "mysql://{}:{}@{}/{}?charset=utf8".format(db_user, db_pass, db_host, db_name)
    engine = create_engine(host_name, echo=False)

    # モデルクラスの基底クラスを作成
    base = declarative_base()

    session_factory = sessionmaker(engine)
    session = scoped_session(session_factory)
except Exception as e:
    print(e);
    print("any error happen")
