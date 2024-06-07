from uiautomator2 import Device
d = Device()
screenshot = d.screenshot("./ccc.jpg")
# screenshot.save("./abc.jpg")
print(screenshot)