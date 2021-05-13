import argparse
import signal
import sys
from concurrent import futures

import grpc
from log import logger

from user.proto import user_pb2_grpc
from user.handler.user import UserService


def exit_server():
    logger.warning("stopping server")
    sys.exit(0)

def serve(port):
    # 初始化一个Grpc server
    server = grpc.server(futures.ThreadPoolExecutor())
    # 向server 注册服务
    user_pb2_grpc.add_UserServicer_to_server(UserService(), server)
    # 运行server
    insecure_port = f"[::]:{port}"
    server.add_insecure_port(insecure_port)

    logger.info(f"server is running with {insecure_port}")

    # 接收退出信号，调用退出函数处理退出逻辑
    signal.signal(signal.SIGINT,exit_server)
    signal.signal(signal.SIGTERM,exit_server)

    server.start()
    # 启动server后，需要让server持续运行，除非手动终止
    server.wait_for_termination()
if __name__ == '__main__':
    pass
