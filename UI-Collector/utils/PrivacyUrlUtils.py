from Config import *

class PrivacyUrlUtils:
    @classmethod
    def save_privacy(cls, data):
        file_name = cls.get_policy_file_path()
        cls.__write_url(file_name, data)

    @staticmethod
    def get_policy_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        policy_path = "PrivacyPolicy"
        policy_file_name = Config.get_instance().get_target_pkg_name() + "-privacyPolicyUrl.txt"
        return os.path.join(config_path, policy_path, policy_file_name)

    @staticmethod
    def __write_url(file_path:str, data:str):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        fw.write(data + "\n")
        fw.close()


