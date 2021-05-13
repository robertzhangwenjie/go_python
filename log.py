import loguru




class Log:
    def __init__(self):
        # 设置日志保存位置,{time}会自动转换为当前的datetime格式
        # 设置每天23点后，在创建日志文件时，会自动重新创建一个日志文件，并将之前的日志按照时间戳明明，日志压缩格式为zip，日志保留时长10天
        self.logger = loguru.logger
        self.logger.add("logs/user.log", rotation="23:00", retention="10 days", compression="zip")

    def get_logger(self):
        return self.logger

logger = Log().get_logger()