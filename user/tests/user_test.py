import datetime
import time
import unittest

import grpc
from google.protobuf import empty_pb2
from user.proto import user_pb2_grpc
from user.proto import user_pb2

class UserServiceTest(unittest.TestCase):

    def setUp(self):
        # 连接grpc服务
        channel = grpc.insecure_channel("127.0.0.1:50050")
        # 初始化一个客户端stub作为客户端
        self.user_stub = user_pb2_grpc.UserStub(channel)

    def test_get_user_list(self):
        # 发起rpc调用
        page_info = user_pb2.PageInfo()
        page_info.pageNum = 1
        page_info.pageSize = 20
        users = self.user_stub.GetUserList(page_info)
        self.assertIsNotNone(users,"get user list failed")

    def test_get_user_by_mobile(self):
        mobile = user_pb2.MobileInfo(mobile = "13995553678")
        user = self.user_stub.GetUserByMobile(mobile)
        self.assertNotEqual(user.id,0)

    def test_get_user_by_id(self):
        user_id = user_pb2.UserId(id = 1)
        user = self.user_stub.GetUserById(user_id)
        self.assertNotEqual(user.id,0)

    def test_create_user(self):
        user = user_pb2.CreateUserInfo()
        user.nickname = "robert"
        user.mobile = "13995553697"
        user.password = "zhangwenjie"

        try:
            res = self.user_stub.CreateUser(user)
            self.assertEqual(res.mobile, user.mobile)
        except grpc.RpcError as e:
            status_code = e.code()
            self.assertEqual(status_code,grpc.StatusCode.ALREADY_EXISTS)

    def test_update_user(self):
        user = user_pb2.UpdateUserInfoReq()
        user.id = 1
        user.nickname = "wenjiezhang"
        user.birthday = int(time.mktime(datetime.date.fromisoformat("1990-08-09").timetuple()))
        user.gender = 0

        self.assertEqual(self.user_stub.UpdateUserInfo(user),empty_pb2.Empty())

if __name__ == '__main__':
    unittest.main()