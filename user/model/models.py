import datetime

import passlib.hash
from peewee import *
from datetime import datetime

from user.config import settings

class BaseMode(Model):
    create_gmt = DateTimeField(default=datetime.now())
    update_gmt = DateTimeField(default=datetime.now())
    class Meta:
        database = settings.db
        legacy_table_name = False


class User(BaseMode):
    '''
    用户模型
    '''
    mobile = CharField(verbose_name="手机号码",max_length=11, index=True,unique=True,null=False)
    passwd = CharField(verbose_name="密码",null=False)
    nick_name = CharField(verbose_name="昵称",null=True,max_length=20)
    avatar_url = CharField(verbose_name="头像地址",null=True)
    birthday = DateField(verbose_name="生日",null=True)
    address = CharField(verbose_name="联系地址",null=True)
    desc = TextField(verbose_name="个人简介",null=True)
    gender = SmallIntegerField(verbose_name="性别",choices=(
        (0,"女"),
        (1, "男")
    ),null=False)
    role = SmallIntegerField(verbose_name="用户角色",choices=(
        (1,"普通用户"),
        (2,"管理员")
    ),default=1)


if __name__ == '__main__':
    users = User.select().paginate(1,5)
    for user in users.dicts():
        print(user)