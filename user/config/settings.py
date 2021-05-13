import logging

from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

class ReconnectMysqlDatabase(ReconnectMixin,PooledMySQLDatabase):
    '''
    使用ReconnectMixin 防止数据库连接断开
    使用PooledMySQLDatabase 使用数据库连接池
    '''
    pass

MYSQL_CONFIG= {
    "host": "www.robertzwj.com",
    "port":3306,
    "database":"go_user",
    "user":"robert",
    "password":"123456"
}

db = ReconnectMysqlDatabase(**MYSQL_CONFIG)

logger = logging.getLogger("peewee")
logger.setLevel(logging.DEBUG)

logger.addHandler(logging.StreamHandler())



