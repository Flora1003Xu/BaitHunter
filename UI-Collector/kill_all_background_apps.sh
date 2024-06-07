#!/bin/bash

# 运行adb shell pm list packages -3命令获取所有第三方应用包名
package_list=$(adb shell pm list packages -3 | cut -d':' -f2)

# 遍历每个包名
for package in $package_list
do
    # 检查应用程序是否在Android设备上运行
    is_running=$(adb shell ps | grep "$package")

    # 如果应用程序在运行，则停止它
    if [ -n "$is_running" ]; then
        echo "Stopping package: $package"
        adb shell am force-stop "$package"
    fi
done
# 另外关闭chrome浏览器，因为其为系统浏览器，不在第三方应用程序列表中
chrome_is_running=$(adb shell ps| grep com.android.chrome)
if [ -n "$chrome_is_running" ];then
    echo "Stopping Chrome..."
    adb shell am force-stop com.android.chrome
fi
echo "Clear done."
exit