import pickle
import os
from Config import *
from StatRecorder import *
from RuntimeContent import RuntimeContent

class SavedInstanceUtils:
    @classmethod
    def dump_pickle(cls, instance):
        file_path = cls.__get_pickle_file_path()
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        f = open(file_path, "wb")
        pickle.dump(instance, f)
        f.close()

    @staticmethod
    def load_pickle(file_path = "./SavedInstance/a.pickle") -> RuntimeContent:
        if not os.path.exists(file_path):
            raise Exception
        f = open(file_path, "rb")
        instance = pickle.load(f)
        f.close()
        return instance

    @staticmethod
    def __get_pickle_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        instance_path = "SavedInstance"
        pickle_file_name = Config.get_instance().get_target_pkg_name() + StatRecorder.get_instance().to_string_result() + ".pickle"
        return os.path.join(config_path, instance_path, pickle_file_name)