import sys
sys.path.append('C:\\Codelife\\ui')
#这样才能找到services,在ui文件夹下面
from services.mislead_detector import check_is_mislead

print(1)
res = check_is_mislead.check_is_mislead_text("发现")
if(res==True):print("true")
else:print("false")
#assert res == False

res = check_is_mislead.check_is_mislead_text("开通会员")
if(res==True):print("true")
else:print("false")
#assert res == False
