# 运行adb shell pm list packages -3命令获取所有第三方应用包名
$package_list = & adb shell pm list packages -3 | ForEach-Object { $_.Split(':')[1].Trim() }

# 遍历每个包名
foreach ($package in $package_list) {
    # 检查应用程序是否在Android设备上运行
    $is_running = & adb shell ps | Select-String $package

    # 如果应用程序在运行，则停止它
    if ($is_running) {
        Write-Host "Stopping package: $package"
        & adb shell am force-stop $package
    }
}

# 另外关闭chrome浏览器，因为其为系统浏览器，不在第三方应用程序列表中
$chrome_is_running = & adb shell ps | Select-String "com.android.chrome"
if ($chrome_is_running) {
    Write-Host "Stopping Chrome..."
    & adb shell am force-stop com.android.chrome
}

Write-Host "Clear done."
Exit