import redis
import configparser


def execute_redis():
    """Redisサーバーの起動を行い,接続したredis-cliを返却する"""
    try:
        config = configparser.ConfigParser()
        config.read('redis.ini')
        redis_host = config["redis-server"]["host"]
        redis_port = config["redis-server"]["port"]
        # 一応typehinを付与
        r: redis.Redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        r.ping()
        return r
    except Exception as e:
        print("--> Redisサーバーの起動に失敗しました")
        print("--> Redisサーバーを起動してください")
        print(type(e))
        print(e.args)
        exit(-1)
