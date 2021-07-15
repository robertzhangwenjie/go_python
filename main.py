import os
import unittest,argparse
from user import server

def arg_parse():
    '''
    解析命令行参数
    :return:
    '''
    # 初始化一个参数解析器
    parser = argparse.ArgumentParser(description="command args parser")

    # user server port
    parser.add_argument(
        "--port",
        nargs="?",
        default=50050,
        type=int,
        help="server port"
    )
    # 对命令行参数进行解析，并返回一个参数对象
    args = parser.parse_args()
    return args


if __name__ == '__main__':


    args = arg_parse()
    server.serve(args.port)