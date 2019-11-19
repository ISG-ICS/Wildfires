class CacheSet(set):
    """
    A Simple Set that used for Cache, will have a memory limitation defined by MAX.

    if more than MAX elements are inserted, elements are popped with regard of insertion order.
    """
    MAX = 1e6

    def add(self, element):
        if self.__len__() >= self.MAX:
            self.pop()
        set.add(self, element)

    def update(self, elements):
        for ele in elements:
            self.add(ele)
