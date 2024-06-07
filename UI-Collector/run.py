from FSM import *
from services.popup_detector import detect_queue
from services.popup_detector.yolo_service import YoloService
from utils.FileUtils import FileUtils
from utils.JsonUtils import *
from utils.SavedInstanceUtils import *
from utils.DrawGraphUtils import *
import sys

def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            LogUtils.log_info('\nKeyboardInterrupt ...')
            LogUtils.log_info('do something after Interrupt ...')
            StatRecorder.get_instance().print_result()
            # StatRecorder.get_instance().print_coverage()
            # RuntimeContent.get_instance().clear_state_list()
            # RuntimeContent.get_instance().clear_screen_list()
            JsonUtils.dump_screen_map_to_json()
            SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())

            # 退出时写入覆盖率
            cur_depth = Config.get_instance().curDepth
            cal_cov_map = StatRecorder.get_instance().get_coverage(cur_depth)
            StatRecorder.get_instance().print_coverage(cal_cov_map)
            if cal_cov_map.get(cur_depth, None) is not None:
                cov = cal_cov_map[cur_depth][1] / cal_cov_map[cur_depth][2]
                FileUtils.save_coverage(cur_depth, cal_cov_map[cur_depth][1], cal_cov_map[cur_depth][2])
                FileUtils.save_result()


            # 绘制App界面跳转图
            if Config.get_instance().isDrawAppCallGraph:
                DrawGraphUtils.draw_callgraph(Config.get_instance().get_CollectDataName())

    sys.excepthook = new_hook


if __name__ == "__main__":
    try:
        pkgName = sys.argv[1]
        appName = sys.argv[2]
        depth = sys.argv[3]
        test_time = sys.argv[4]
        searchPP = sys.argv[5]
        drawAppCallGraph = sys.argv[6]
        ScreenUidRep = sys.argv[7]
        #读取命令行参数，设置Config实例参数
        Config.get_instance().target_pkg_name = pkgName
        Config.get_instance().app_name = appName
        Config.get_instance().maxDepth = int(depth)
        Config.get_instance().test_time = int(test_time)
        if drawAppCallGraph == 'true':
            DrawAppCallGraph = True
        else:
            DrawAppCallGraph = False
        Config.get_instance().isDrawAppCallGraph = DrawAppCallGraph
        if searchPP == 'true':
            searchPP = True
        else:
            searchPP = False
        Config.get_instance().isSearchPrivacyPolicy = searchPP
        Config.get_instance().ScreenUidRep = ScreenUidRep
    except IndexError:
        print('No arg mode.')



    # with open('tmp.txt', 'w',encoding='utf-8') as f:
    #     f.write(pkgName + ";" + appName + ";" + depth + ';' + test_time + ';' + searchPP + ';' + drawAppCallGraph + ';' + ScreenUidRep )

    # 创建一个阻塞队列 78-85
    pp_queue = None

    LogUtils.setup()

    if Config.get_instance().is_saved_start:
        runtime = SavedInstanceUtils.load_pickle(Config.get_instance().get_pickle_file_name())
        root = runtime.screen_map["root"]
    else:
        root = ScreenNode()
        root.ck_eles_text = "root"
        RuntimeContent.get_instance().set_last_screen_node(root)
        RuntimeContent.get_instance().set_last_clickable_ele_uid("dummy_root_element")
        RuntimeContent.get_instance().put_screen_map("root", root)

    suppress_keyboard_interrupt_message()

    # 计时开始
    StatRecorder.get_instance().set_start_time()
    restart_cnt = 0

    
    queue = Queue() 
    req_queue = Queue(1)
    resp_queue = Queue(1)
    yolo_service = YoloService('YoloDetectPopupService', req_queue, resp_queue, True)

    # 启动app
    d = Config.get_instance().get_device()

    d.app_start(Config.get_instance().get_target_pkg_name(), use_monkey=True)


    yolo_service.start()

    RuntimeContent.get_instance().set_last_screen_node(root)
    RuntimeContent.get_instance().set_last_clickable_ele_uid("dummy_root_element")
    time.sleep(10)



    # 控制FSM线程, 重启会继续运行
    while True:
        # FSM开始运行
        consumer_fsm = FSM('FSM', queue, req_queue, resp_queue,pp_queue)
        consumer_fsm.start()
        consumer_fsm.join()

        # fsm线程触发了RestartException
        if consumer_fsm.exit_code == 1:
            StatRecorder.get_instance().inc_restart_cnt()
            LogUtils.log_info("需要重启")
            # logging.exception(consumer_fsm.exception)
            # logging.exception(consumer_fsm.exc_traceback)
            StatRecorder.get_instance().print_result()
            # SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())

            # 重启
            d.app_stop(Config.get_instance().get_target_pkg_name())
            time.sleep(1)
            d.app_start(Config.get_instance().get_target_pkg_name(), use_monkey=True)

            # # 重启frida
            # restart_thread(frida_hook_service)

            time.sleep(5)
            RuntimeContent.get_instance().set_last_screen_node(root)
            RuntimeContent.get_instance().set_last_clickable_ele_uid("dummy_root_element")
        # fsm线程触发了TerminateException
        elif consumer_fsm.exit_code == 2:
            LogUtils.log_info("程序正常结束")
            break
        elif consumer_fsm.exit_code == 3:
            LogUtils.log_info("程序超时退出")
            # logging.exception(consumer_fsm.exception)
            # logging.exception(consumer_fsm.exc_traceback)
            break
        # fsm线程触发了未知错误
        else:
            LogUtils.log_info("未知情况退出")
            LogUtils.log_info(consumer_fsm.exception)
            LogUtils.log_info(consumer_fsm.exc_traceback)
            logging.exception(consumer_fsm.exception)
            break

    # 程序收尾
    StatRecorder.get_instance().print_result()
    JsonUtils.dump_screen_map_to_json()
    SavedInstanceUtils.dump_pickle(RuntimeContent.get_instance())

    # 退出时写入覆盖率
    cur_depth = Config.get_instance().curDepth
    cal_cov_map = StatRecorder.get_instance().get_coverage(cur_depth)
    StatRecorder.get_instance().print_coverage(cal_cov_map)
    if cal_cov_map.get(cur_depth, None) is not None:
        cov = cal_cov_map[cur_depth][1] / cal_cov_map[cur_depth][2]
        FileUtils.save_coverage(cur_depth, cal_cov_map[cur_depth][1], cal_cov_map[cur_depth][2])

    # 写入总的覆盖率
    total_cov_map = StatRecorder.get_instance().get_total_coverage()
    FileUtils.save_total_coverage(Config.get_instance().maxDepth, total_cov_map)


    FileUtils.save_result()


    # 绘制App界面跳转图
    if Config.get_instance().isDrawAppCallGraph:
        DrawGraphUtils.draw_callgraph(Config.get_instance().get_CollectDataName())

