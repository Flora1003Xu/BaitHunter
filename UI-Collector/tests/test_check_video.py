import subprocess

# 执行 adb shell 命令获取当前媒体会话信息
cmd = "adb shell dumpsys media_session"
process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

# 解析媒体会话信息，查找包含 "PlaybackState" 和 "state=3" 的行
for line in output.decode().split('\n'):
    if "PlaybackState" in line and "state=3" in line:
        print("Pixel 3 is currently playing a video.")
        break
else:
    print("Pixel 3 is not currently playing a video.")
