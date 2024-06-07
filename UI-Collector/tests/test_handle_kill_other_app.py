from StateHandler import *

content = {}
content["cur_screen_pkg_name"] = "com.sina.weibo"
Config.get_instance().target_pkg_name =  "com.taobao.taobao"
StateHandler.handle_kill_other_app(content)