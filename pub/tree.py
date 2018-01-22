#! python3
# coding: utf-8

class Node():
    sep = "/"
    def __init__(self,name):
        self._name = name
        self._parent = None
        self._children = []

    def __repr__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,parent):
        self._parent = parent

    @property
    def children(self):
        return self._children

    @property
    def path(self):
        current = self
        nodes = [current.name]
        while True :
            p = current.parent
            if p :
                nodes.append(p.name)
                current = p
            else :
                break
        nodes.reverse()
        ret = Node.sep.join(nodes)
        return ret

    def add(self,child):
        self._children.append(child)
        child.parent = self
        return child

    def insert(self,target,child):
        if target in self._children :
            self.remove(target)
            self.add(child)
            child.add(target)

    def remove(self,child):
        if child in self._children :
            self._children.remove(child)
            child.parent = None
            return child
        return None

    def remove_all(self):
        for child in self._children :
            child.parent = None

        return self._children.clear()

    def find(self,name):
        return self._search(name)

    def _search(self,name):
        ret = None
        for child in self._children :
            if child.name == name :
                ret = child
                break
            else :
                ret = child._search(name)
                if ret :
                    break
        return ret

    def find_all(self,name):
        res = []
        self._search_all(res,name)
        return res

    def _search_all(self,res,name):
        for child in self._children :
            if child.name == name :
                res.append(child)

            child._search_all(res,name)


if __name__ == "__main__":
    root = Node("root")
    a1 = Node("a1")
    a2 = Node("a2")
    a3 = Node("a3")
    b1 = Node("b1")
    b2 = Node("b2")
    c1 = Node("c1")
    c2 = Node("c2")
    root.add(a1)
    root.add(a2)
    root.add(a3)
    a2.add(b1)
    a2.add(b2)
    b1.add(c1)
    print(c1.path)
    b1.insert(c1,c2)
    print(c1.path)

