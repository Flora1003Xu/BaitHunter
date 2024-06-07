# from services.mislead_detector.get_mislead_eles import get_mislead_eles
# result=get_mislead_eles("1.png")
# print(result)
import filecmp

photo1_path = "1.png"
photo2_path = "3.png"

if filecmp.cmp(photo1_path, photo2_path):
    print("The two photos are the same.")
else:
    print("The two photos are different.")

