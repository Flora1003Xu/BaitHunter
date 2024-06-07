import pickle
class TestClass:
    def __init__(self, name):
        self.name=name
        self.child = []



test_dict = {}
A = TestClass("nihao")
B = TestClass("wuyu")
test_dict[0] = A
A.child.append(B)
print(A.child[0])
C = TestClass("meme")
B.child.append(C)
test_dict[1] = B

f = open('somedata', 'wb')
pickle.dump(test_dict, f)
f.close()



f = open('somedata', 'rb')
res = pickle.load(f)
print(res[0].child[0])
print(res[1])
f.close()
