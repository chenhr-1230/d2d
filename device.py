import cache


class Device:

    # 根据缓存能力和算法确定缓存决策
    def set_cache(self, cache_capacity, caching_algorithm):
        if caching_algorithm == "DRL":
            self.cache = cache.DRL_Cache(cache_capacity)
        # elif caching_algorithm == "MLPLRU":
        #     self.cache = cache.MLPLRU_Cache(cache_capacity)
        # elif caching_algorithm == "Cache-Me-Cache":
        #     self.cache = cache.Cache_Me_Cache(cache_capacity)


class EdgeSever(Device):
    # 初始化基站的属性
    def __init__(self, cache_capacity, caching_algorithm, range):
        self.range = range
        self.set_cache(cache_capacity, caching_algorithm)



class Mobile(Device):
    # 初始化移动设备属性
    def __init__(self, id, cache_capacity, caching_algorithm, range):
        self.id = id
        self.range = range
        self.set_cache(cache_capacity, caching_algorithm)
