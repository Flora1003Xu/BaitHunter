from RuntimeContent import *

A = RuntimeContent.get_instance().get_screen_map()
print(A)
A["aaaa"] = "vvvv"
B = RuntimeContent.get_instance().get_screen_map()
print(B)
# RuntimeContent.get_instance().put_screen_map("aa", "bb")

print(A)