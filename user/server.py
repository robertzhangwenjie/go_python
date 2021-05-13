import logging
from concurrent import futures
import grpc

from user.proto import user_pb2_grpc
from user.handler.user import UserService


def serve():
    # 初始化一个Grpc server
    server = grpc.server(futures.ThreadPoolExecutor())
    # 向server 注册服务
    user_pb2_grpc.add_UserServicer_to_server(UserService(), server)
    # 运行server
    insecure_port = "[::]:50050"
    server.add_insecure_port(insecure_port)
    logging.log(logging.WARNING,f"server is running with {insecure_port}")
    server.start()
    # 启动server后，需要让server持续运行，除非手动终止
    server.wait_for_termination()
if __name__ == '__main__':
    logging.basicConfig(filename="logs/log.txt")
    serve()
