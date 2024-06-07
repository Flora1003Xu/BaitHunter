class UITreeNode:
    def __init__(self):
        self.name = None
        self.childs = []
        self.isDir = False

    def __init__(self, name):
        self.name = name
        self.childs = []
        self.isDir = False

    def __eq__(self, other):
        return self.name == other.name and self.isDir == other.isDir and self.childs == other.childs

    def __lt__(self, other):
        if self.isDir != other.isDir:
            return self.isDir > other.isDir
        else:
            return self.name < other.name






