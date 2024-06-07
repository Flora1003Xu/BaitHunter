import os.path

from uiautomator2 import Device
from datetime import datetime


# "com.autonavi.minimap" # 高德地图
# "com.ss.android.ugc.aweme" #抖音
# "net.csdn.csdnplus"
# "com.sina.weibo"
# "com.youku.phone"
# "cn.damai"
# "com.ss.android.lark"
# "com.cloudy.component"
# "com.jingyao.easybike"
# "com.cainiao.wireless"
# "com.xingin.xhs"
# "com.yipiao"
# "app.podcast.cosmos"
# "com.hunantv.imgo.activity"
# "tv.danmaku.bili" #b站
# "com.netease.edu.ucmooc" #MOOC
# "com.cainiao.wireless" #菜鸟
# "com.taobao.taobao" #淘宝
# "com.taobao.mobile.dipei"#口碑
# "com.taobao.trip"#飞猪旅行
# "com.youku.phone"#优酷视频
# "com.eg.android.AlipayGphone"#支付宝
# "com.xiaomi.smarthome" #米家
# "me.ele" #饿了么
# "com.alibaba.wireless.lstretailer" # 阿里零售通
# "com.alibaba.cloudmail" # 阿里邮箱
# ”com.taobao.aliAuction“  #阿里拍卖
# "com.alibaba.aliyun" # 阿里云
# "com.alicloud.databox" # 阿里云盘
# "com.wudaokou.hippo" # 盒马
# "com.moji.mjweather" # 墨迹天气
# "com.alibaba.android.rimet" #钉钉
# "com.taobao.idlefish" # 闲鱼
# "com.alimama.moon" # 淘宝联盟
# "com.shuqi.controller" # 书旗小说
# "com.taobao.qianniu" # 千牛
# "com.UCMobile" # UC浏览器
# "com.taobao.etao" # 一淘
# "com.tmall.wireless" # 手机天猫
# "com.taobao.movie.android" # 淘票票
# “com.antfortune.wealth” # 蚂蚁财富
# “com.mybank.android.phone” # 网商银行

class Config(object):
    def __init__(self):
        # with open('tmp.txt', 'r', encoding='utf-8') as f:
        #     pkgName, appName, depth, test_time,searchPP,drawAppCallGraph,ScreenUidRep = f.readline().split(";")
        # print(pkgName, appName, depth, test_time,searchPP,drawAppCallGraph,ScreenUidRep)

        # # 其余可修改的配置，从此处开始===========================
        # self.target_pkg_name = pkgName  # 应用包名
        # self.app_name = appName  # 应用名
        # self.maxDepth = int(depth)  # 配置点击的最大深度
        #
        # self.curDepth = 1
        # self.test_time = int(test_time)  # 配置测试的时间,以秒为单位
        # # self.isSearchPrivacyPolicy = False # 配置是否寻找隐私政策
        # # self.isDrawAppCallGraph = False  # 配置是否绘制App界面跳转图
        # if searchPP == 'true':
        #     self.isSearchPrivacyPolicy = True
        # else:
        #     self.isSearchPrivacyPolicy = False
        #
        # self.sleep_time_sec = 0.3  # 配置点击之后睡眠的时间
        #
        # if drawAppCallGraph == 'true':
        #     self.isDrawAppCallGraph = True
        # else:
        #     self.isDrawAppCallGraph = False
        self.target_pkg_name = 'me.ele'
        self.app_name = '饿了么'  # 应用名
        self.maxDepth = 3  # 配置点击的最大深度

        self.curDepth = 1


        self.sleep_time_sec = 2  # 配置点击之后睡眠的时间
        # self.isSearchPrivacyPolicy = False # 配置是否寻找隐私政策
        # self.isDrawAppCallGraph = False  # 配置是否绘制App界面跳转图
        self.isSearchPrivacyPolicy = False


        self.sleep_time_sec = 1.5  # 配置点击之后睡眠的时间

        # 到此处结束===========================================
        # 下面的配置不要修改

        self.CLICK_MAX_CNT = 4
        self.device = None
        self.screen_similarity_threshold = 0.7  # 配置界面与界面之间相似度多少表示同一界面, 默认90%/0.9
        self.UndefineDepth = 100000
        self.root_path = "collectData"
        self.start_time = datetime.now().strftime("%Y%m%d-%H%M%S")

        # ScreenUid的表示方式


        # self.ScreenUidRep = "loc" # ex:[loc, textloc]
        self.ScreenUidRep = 'loc'
        self.privacy_policy_text_list = ["隐私权政策", "隐私政策", "隐私保护政策", "隐私保护指引"]

        self.use_pickle_file_name = "./collectData/com.alibaba.aliyun-20231103-002136/SavedInstance/com.alibaba.aliyun_restart17activity21&screen148&time2062.93s.pickle"
        self.is_saved_start = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            Config._instance = object.__new__(cls)
        return Config._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Config, '_instance'):
            Config._instance = Config(*args, **kwargs)
        return Config._instance

    def get_target_pkg_name(self):
        return self.target_pkg_name

    def get_CLICK_MAX_CNT(self):
        return self.CLICK_MAX_CNT

    def get_sleep_time_sec(self):
        return self.sleep_time_sec

    def get_log_file_name(self):
        return self.log_file_name

    def get_pickle_file_name(self):
        return self.use_pickle_file_name

    def set_device(self, device):
        self.device = device

    def get_device(self):
        if self.device is None:
            self.set_device(Device())
        return self.device

    def get_CollectDataName(self):
        return self.target_pkg_name + "-" + self.start_time

    def get_collectDataPath(self):
        pkg_path = self.target_pkg_name + "-" + self.start_time
        return os.path.join(self.root_path, pkg_path)
