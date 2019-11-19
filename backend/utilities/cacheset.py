class CacheSet(set):
    """
    A Simple Set that used for Cache, will have a memory limitation defined by MAX.

    if more than MAX elements are inserted, elements are popped with regard of insertion order.
    """
    MAX = 1e6

    def __init__(self, s=(), maximum_size=MAX):
        super(CacheSet, self).__init__(s)
        self.maximum_size = maximum_size

    def add(self, element):
        if self.__len__() >= self.maximum_size:
            self.pop()
        set.add(self, element)

    def update(self, elements):
        for ele in elements:
            self.add(ele)
