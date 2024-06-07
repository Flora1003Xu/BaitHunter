from utils.JsonUtils import dump_screen_map_to_json
from utils.SavedInstanceUtils import *

Config.get_instance().target_pkg_name = "com.alibaba.android.rimit"
StatRecorder.get_instance().start_time = time.time()
StatRecorder.get_instance().end_time = time.time()
dump_screen_map_to_json()

