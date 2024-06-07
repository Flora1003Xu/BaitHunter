import logging
import sys
from logging import StreamHandler
from logging import FileHandler
import os
from Config import *

class LogUtils:
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(LogUtils, "_instance"):
    #         LogUtils._instance = object.__new__(cls)
    #     return LogUtils._instance
    #
    # @classmethod
    # def get_instance(cls, *args, **kwargs):
    #     if not hasattr(LogUtils, '_instance'):
    #         LogUtils._instance = LogUtils(*args, **kwargs)
    #     return LogUtils._instance
    file_path = ""
    logger = logging.getLogger(__name__)
    logger.propagate = False

    @classmethod
    def setup(cls):
        cls.file_path = cls.__get_log_file_path()
        cls.__create_dir()
        cls.__set_logger()

    @staticmethod
    def __get_log_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        log_path = "Log"
        log_file_name = Config.get_instance().get_target_pkg_name() + ".log"
        return os.path.join(config_path, log_path, log_file_name)

    @classmethod
    def log_info(cls, msg):
        cls.logger.info(msg)

    @classmethod
    def log_error(cls, msg):
        cls.logger.error(msg)

    # def __init__(self):
    #     self.file_path = ""
    #     self.logger = logging.getLogger(__name__)
    #     # self.rewrite_print = print

    @classmethod
    def __create_dir(cls):
        if not os.path.exists(os.path.dirname(cls.file_path)):
            os.makedirs(os.path.dirname(cls.file_path))

    @classmethod
    def __add_stream_handler(cls):
        # 标准流处理器，设置的级别为WARAING
        stream_handler = StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(logging.INFO)
        format = logging.Formatter('%(message)s')
        stream_handler.setFormatter(format)
        cls.logger.addHandler(stream_handler)

    @classmethod
    def __add_file_handler(cls):
        file_handler = FileHandler(filename=cls.file_path)
        file_handler.setLevel(logging.INFO)
        format = logging.Formatter('%(message)s')
        file_handler.setFormatter(format)
        cls.logger.addHandler(file_handler)

    @classmethod
    def __set_logger(cls):
        cls.__add_stream_handler()
        cls.__add_file_handler()
        cls.logger.setLevel(logging.DEBUG)
        # self.logger.setformatter('%(message)s')







