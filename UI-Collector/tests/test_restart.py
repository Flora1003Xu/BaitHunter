import time
from uiautomator2 import Device

# device_serial = "52dd3cc5"
# d = u2.connect(device_serial) # alias for u2.connect_usb('123456f')
# print(d.info)
d = Device()
print(d.info)
# target_pkg_name = "com.alibaba.android.rimet"
target_pkg_name = "com.alibaba.wireless.lstretailer"
# d.app_stop(target_pkg_name)

# d.app_clear(target_pkg_name)

while True:
    pid = d.app_start(target_pkg_name, use_monkey=True)  # 等待应用运行, return pid(int)
    time.sleep(10)
    cnt = 0
    for i in range(0, 100000):
        cnt +=1
    print("ok")
    d.app_stop(target_pkg_name)
    time.sleep(10)

