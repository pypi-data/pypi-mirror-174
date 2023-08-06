"""
@author axiner
@version v1.0.0
@created 2022/10/28 14:23
@abstract redis
@description
@history
"""
try:
    import redis
except ImportError:
    raise

__all__ = [
    'Rds',
]


class Rds:
    """
    redis连接池
    使用示例：
        r = Rds(host='127.0.0.1')
        # 或
        with Rds(host='127.0.0.1') as r:
            pass
        +++++[更多详见参数或源码]+++++
    """

    def __init__(
            self,
            host="localhost",
            port=6379,
            db=0,
            password=None,
            **kwargs,
    ):
        """
        初始化连接
        :param host: host
        :param port: 端口
        :param db: 数据库
        :param password: 密码
        :param kwargs: 其他参数
        """
        _redis_pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            **kwargs,
        )
        self._conn = redis.Redis(connection_pool=_redis_pool)

    def __getattr__(self, cmd):
        def _(*args, **kwargs):
            return getattr(self._conn, cmd)(*args, **kwargs)
        return _

    def __enter__(self):
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.close()
        else:
            return True
