import redis
import configparser


class RedisCli:
    """redis-serverへの接続を行う"""

    def __init__(self, host: str, port: int, db: int):
        self.redis = None
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        self.redis = redis.Redis(host=self.host, port=self.port, db=self.db)
        return self.redis


def execute_redis():
    """Redisサーバーの起動を行い,接続したredis-cliを返却する"""
    try:
        config = configparser.ConfigParser()
        config.read('redis.ini')
        rc = RedisCli(
            host=config["redis-server"]["host"],
            port=int(config["redis-server"]["port"]),
            db=0)
        r = rc.connect();
        r.ping();
        return r
    except Exception as e:
        print("--> Redisサーバーの起動に失敗しました")
        print("--> Redisサーバーを起動してください")
        print(type(e))
        print(e.args)
        exit(-1)
