from utils.SavedInstanceUtils import *
from RuntimeContent import *
Config.get_instance().target_pkg_name = "com.alibaba.android.rimit"
StatRecorder.get_instance().start_time = time.time()
StatRecorder.get_instance().end_time = time.time()
file = SavedInstanceUtils.get_pickle_file_path()
SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())
