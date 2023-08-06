"""
@author axiner
@version v1.0.0
@created 2022/10/28 14:03
@abstract 锁
@description
@history
"""
import time

__all__ = [
    'Locker',
]


class Locker:
    """
    锁，基于redis的分布式锁
    使用示例：
        a = 0
        locker = Locker(redis_client)  # 创建锁实例
        if locker.acquire(acquire_timeout=2)  # 获取锁
            for i in range(10):
                a += 1
                print(f'a: {a}')
            locker.release()  # 释放锁

        # 另：with方式
        a = 0
        locker = Locker(redis_client, acquire_timeout=2)
        with locker:
            if locker.is_lock:  # 若获取锁
                for i in range(10):
                    a += 1
                    print(f'a: {a}')
        +++++[更多详见参数或源码]+++++
    """

    def __init__(
            self,
            redis_client,
            acquire_timeout: int = 2,
            timeout: int = 10,
            lock_name: str = 'locker',
            lock_value: str = 'locker!@#',
    ):
        """
        锁，基于redis实现（可用于分布式）
        :param redis_client: redis客户端对象
        :param acquire_timeout: 获取锁的超时时间
        :param timeout: 锁的过期时间
        :param lock_name: 锁名
        :param lock_value: 锁值
        """
        self.rds = redis_client
        self.acquire_timeout = acquire_timeout
        self.timeout = timeout
        self.lock_name = lock_name if lock_name else 'locker'
        self.lock_value = lock_value if lock_value else 'locker!@#'
        self.list_key = f'{self.lock_name}-list'
        self.is_lock = False

    def acquire(
            self,
            acquire_timeout: int = None,
            timeout: int = None,
            lock_name: str = None,
            lock_value: str = None,
    ) -> bool:
        """
        获取锁
        :param acquire_timeout: 获取锁的超时时间
        :param timeout: 锁的过期时间
        :param lock_name: 锁名
        :param lock_value: 锁值
        :return:
        """
        if acquire_timeout is not None:
            self.acquire_timeout = acquire_timeout
        if timeout is not None:
            self.timeout = timeout
        if lock_name:
            self.lock_name = lock_name
            self.list_key = f'{self.lock_name}-list'
        if lock_value:
            self.lock_value = lock_value
        end_time = time.time() + self.acquire_timeout
        while time.time() < end_time:
            if self._lock_key():
                return self.is_lock
            if self._lock_list():
                return self.is_lock
            time.sleep(0.01)
        return self.is_lock

    __enter__ = acquire

    def _lock_key(self):
        if self.rds.set(self.lock_name, self.lock_value, ex=self.timeout, nx=True):
            self.is_lock = True
        return self.is_lock

    def _lock_list(self):
        self._set_expire()
        list_top = self.rds.blpop(self.list_key, self.timeout)
        if list_top is not None:
            self.is_lock = True
            self.rds.set(self.lock_name, self.lock_value)
            self._set_expire()
        return self.is_lock

    def _set_expire(self):
        self.rds.expire(self.lock_name, self.timeout)
        self.rds.expire(self.list_key, self.timeout)

    def release(self):
        """释放锁"""
        if self.is_lock:
            self._set_expire()
            if self.rds.get(self.lock_name) == self.lock_value:
                self.rds.lpush(self.list_key, self.lock_value)
                self._set_expire()

    def __exit__(self, t, v, tb):
        self.release()
