import datetime
import time

import grpc

from user.proto import user_pb2_grpc
from user.proto import user_pb2
from user.model import models

class UserService(user_pb2_grpc.UserServicer):
    def GetUserList(self, request: user_pb2.PageInfo, context):
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
        for user  in users.paginate(pageNum,pageSize):
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


    def GetUserByMobile(self, request, context):
        return super().GetUserByMobile(request, context)

    def GetUserById(self, request, context):
        return super().GetUserById(request, context)

    def CreateUser(self, request, context):
        return super().CreateUser(request, context)

    def UpdateUserInfo(self, request, context):
        return super().UpdateUserInfo(request, context)



if __name__ == '__main__':
   pass