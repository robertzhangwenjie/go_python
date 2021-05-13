import unittest

import grpc

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

if __name__ == '__main__':
    unittest.main()