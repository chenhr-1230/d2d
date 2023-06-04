import math


class Cell:
    def __init__(self):
        self.devices = []


class Terrain:

    def __init__(self, size):
        self.size = size
        self.mobiles = [] #用来记录所有移动设备
        self.self_hit, self.d2d_hit, self.es_hit, self.sat_hit, self.miss = 0, 0, 0, 0, 0
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)] #用来记录所有的设备包括位置信息

    def clear_caches(self):
        self.self_hit, self.d2d_hit, self.es_hit, self.sat_hit, self.miss = 0, 0, 0, 0, 0
        self.edge_sever.cache.clear()
        for m in self.mobiles:
            m.cache.clear()

    def locate_device(self, device, x, y):
        self.cells[x][y].devices.append(device)


    def add_edge_station(self, edge_sever):
        self.edge_sever = edge_sever
        self.locate_device(self.edge_sever, self.edge_sever.x, self.edge_sever.y)

    def add_mobile(self, mobile):
        self.mobiles.append(mobile)
        self.locate_device(mobile, mobile.x, mobile.y)

    # 计算两个设备之间的距离
    def distance_between(self, device1, device2):
        return math.sqrt((device1.x - device2.x) ** 2 + (device1.y - device2.y) ** 2)

    # 判断两个设备之间是否能够进行通信
    def can_communicate(self, device, other_device):
        return self.distance_between(device, other_device) < min(device.range, other_device.range)

    # 当请求的特定内容已缓存在邻居节点中时，返回Ture
    def contains_in_neighbours(self, user, content):
        for m in self.mobiles:
            if self.can_communicate(user, m):
                if m.cache.contains(content):
                    m.cache.new_content(content)
                    return True

        return False

    # 当请求的特定内容已缓存在边缘服务器中时，返回Ture
    def contains_in_edge_sever(self, user, content):
        if self.can_communicate(user, self.edge_sever):
            if self.edge_sever.cache.contains(content):
                self.edge_sever.cache.new_content(content)
                return True

        return False

    # def contains_in_satellite(self, content):
    #     if self.satellite.cache.contains(content):
    #         self.satellite.cache.new_content(content)
    #         return True
    #
    #     return False

    def content_request(self, user, content):
        # 本地缓存命中
        if user.cache.contains(content):
            self.self_hit += 1

        # d2d缓存命中
        elif self.contains_in_neighbours(user, content):
            self.d2d_hit += 1

        # 边缘服务器命中
        elif self.contains_in_edge_sever(user, content):
            self.es_hit += 1


        else:
            # 缓存机制，未完
            if self.can_communicate(user, self.edge_sever):
                self.edge_sever.cache.new_content(content)

            self.miss += 1

        # 缓存该内容
        user.cache.new_content(content)
