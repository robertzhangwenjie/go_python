import datetime
import hashlib
import time

import grpc
import passlib.hash
from peewee import DoesNotExist
from google.protobuf import empty_pb2

from log import logger
from user.proto import user_pb2_grpc
from user.proto import user_pb2
from user.model import models


class UserService(user_pb2_grpc.UserServicer):

    @logger.catch
    def convert_user_to_res(self, user):
        '''
        将返回的user对象转换为res对象
        :param user: User实例对象
        :param res: UserInfoResponse对象
        :return:
        '''

        res = user_pb2.UserInfoResponse()

        res.id = user.id
        res.password = user.passwd
        if user.gender:
            res.gender = user.gender
        if user.nick_name:
            res.nickname = user.nick_name
        if user.address:
            res.address = user.address
        if user.desc:
            res.desc = user.desc
        res.role = user.role
        res.mobile = user.mobile

        if user.birthday:
            res.birthday = int(time.mktime(user.birthday.timetuple()))

        return res

    @logger.catch
    def GetUserList(self, request, context):
        # 初始化返回的消息体对象
        res = user_pb2.UserListResponse()
        # 获取所有用户信息
        users = models.User.select()
        # 获取用户总数量
        res.total = users.count()
        # 根据分页查询
        pageSize = 10
        pageNum = 1
        if request.pageNum:
            pageNum = request.pageNum
        if request.pageSize:
            pageSize = request.pageSize
        for user in users.paginate(pageNum, pageSize):
            # 将每一个用户信息转换为定义的rpc message 对象
            user_info = user_pb2.UserInfoResponse()
            user_info.id = user.id
            user_info.password = user.passwd
            user_info.role = user.role
            user_info.gender = user.gender
            user_info.mobile = user.mobile

            # 针对可以为空的字段需要进行判断，避免将None赋值给proto中定义的字段
            # if user.nick_name:
            #     user_info.nickname = user.nick_name
            # else:
            #     user_info.nickname = ""
            #
            # if user.desc:
            #     user_info.desc = user.desc
            # else:
            #     user_info.desc = ""
            #
            # if user.address:
            #     user_info.address = user.address
            # else:
            #     user_info.address = ""

            if user_info.birthday:
                # 将日期转换为时间戳
                user_info.birthday = int(time.mktime(user.birthday.timetuple()))
            else:
                user_info.birthday = 0

            res.data.append(user_info)

        context.set_code(grpc.StatusCode.OK)
        return res

    @logger.catch
    def GetUserByMobile(self, request, context):
        res = user_pb2.UserInfoResponse()

        try:
            user = models.User.get(models.User.mobile == request.mobile)
            res = self.convert_user_to_res(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("no such user")

        return res

    @logger.catch
    def GetUserById(self, request, context):
        res = user_pb2.UserInfoResponse()

        try:
            user = models.User.get_by_id(request.id)
            res = self.convert_user_to_res(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("no such user")

        return res

    @logger.catch
    def CreateUser(self, request: user_pb2.CreateUserInfo, context):
        res = user_pb2.UserInfoResponse()

        # whether the user is exist or not
        user = models.User.get_or_none(models.User.mobile == request.mobile)
        if user is not None:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("user already exists")
            return res

        user = models.User.create(nick_name=request.nickname, mobile=request.mobile,
                                  passwd=passlib.hash.pbkdf2_sha256.hash(request.password))
        res = self.convert_user_to_res(user)
        return res

    @logger.catch
    def UpdateUserInfo(self, request: user_pb2.UpdateUserInfoReq, context):

        # whether the user already exists
        try:
            user = models.User.get_by_id(request.id)
            user.nick_name = request.nickname
            user.gender = request.gender
            user.birthday = datetime.date.fromtimestamp(request.birthday)
            user.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("no such user")
            return empty_pb2.Empty()


if __name__ == '__main__':
    pass
