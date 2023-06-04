import terrain
import device
import content
import random

from parameters import *


class Simulator:

    def __init__(self):
        # 初始化场景
        self.terrestrial = terrain.Terrain(TERRAIN_SIZE)
        # 初始化边缘服务器,包含便于服务器的位置、储存容量、缓存决策
        self.place_edge_sever()
        # 初始化移动设备
        self.place_mobiles_randomly(NUMBER_OF_USERS)
        # 初始化请求内容（Zipf分布）
        self.contents = content.generate_zipf_content(NUMBER_OF_CONTENTS, CONTENT_SIZE, ZIPF_PARAMETER)

    def place_edge_sever(self):
        edge_sever = device.EdgeSever(EDGE_SEVER_CACHE_CAPACITY, "DRL", EDGE_SEVER_RANGE)
        # 将边缘服务器设置为场景的中央
        edge_sever.x = int(TERRAIN_SIZE / 2)
        edge_sever.y = int(TERRAIN_SIZE / 2)
        self.terrestrial.add_edge_station(edge_sever) # 完成边缘服务器的添加


    def place_mobiles_randomly(self, number_of_users):
        for i in range(number_of_users):
            new_mobile = device.Mobile(i, MOBILE_CACHE_CAPACITY, "DRL", MOBILE_RANGE)
            new_mobile.x = random.randint(0, TERRAIN_SIZE - 1)  # x 坐标
            new_mobile.y = random.randint(0, TERRAIN_SIZE - 1)  # y 坐标
            self.terrestrial.add_mobile(new_mobile)  # 完成移动设备的添加

    def print_cache_stats(self, message):
        print(message)
        print("Number of contents:                  {}".format(len(self.contents)))
        print("Number of self cache hits:           {}".format(self.terrestrial.self_hit))
        print("Number of d2d cache hits:            {}".format(self.terrestrial.d2d_hit))
        print("Number of edge sever cache hits:   {}".format(self.terrestrial.es_hit))
        print("Number of cache miss:                {}".format(self.terrestrial.miss))
        # print("-------------------------------------------")
        # print(self.terrestrial.mobiles[15].__dict__)
        # print("-------------------------------------------")
        # print(self.terrestrial.mobiles[15].cache.__dict__)
        # print("-------------------------------------------")
        # es = self.terrestrial.cells[250][250].__dict__
        # print(es['devices'][0].__dict__)
        # print("-------------------------------------------")
        # print(es['devices'][0].cache.__dict__)

    # 随机地选择用户发起内容请求
    def request_contents_randomly(self):
        for c in self.contents:
            user = random.choice(self.terrestrial.mobiles)
            self.terrestrial.content_request(user, c)

    # # 返回缓存命中率以及内容的数目
    # def num_contents_test(self, algorithm, num_contents):
    #     self.terrestrial.clear_caches()
    #     self.terrestrial.edge_sever.set_cache(EDGE_SEVER_CACHE_CAPACITY, algorithm)
    #
    #     for mobile in self.terrestrial.mobiles:
    #         mobile.set_cache(MOBILE_CACHE_CAPACITY, algorithm)
    #
    #     self_hits = []
    #     d2d_hits = []
    #     es_hits = []
    #     sat_hits = []
    #     universal = []
    #
    #     for i in range(len(self.contents)):
    #         user = random.choice(self.terrestrial.mobiles)
    #         self.terrestrial.content_request(user, self.contents[i])
    #
    #         if i+1 in num_contents:
    #             self_hits.append(self.terrestrial.self_hit / i)
    #             d2d_hits.append(self.terrestrial.d2d_hit / i)
    #             es_hits.append(self.terrestrial.es_hit / i)
    #             universal.append(self.terrestrial.miss / i)
    #
    #     return self_hits, d2d_hits, es_hits, sat_hits, universal
    #
    #
    # def zipf_test(self, algorithm, zipf_values):
    #     self.terrestrial.clear_caches()
    #     self.terrestrial.edge_sever.set_cache(EDGE_SEVER_CACHE_CAPACITY, algorithm)
    #
    #     for mobile in self.terrestrial.mobiles:
    #         mobile.set_cache(MOBILE_CACHE_CAPACITY, algorithm)
    #
    #     self_hits = []
    #     d2d_hits = []
    #     bs_hits = []
    #     universal = []
    #
    #     for value in zipf_values:
    #         self.contents = content.generate_zipf_content(NUMBER_OF_CONTENTS, CONTENT_SIZE, value)
    #         for i in range(len(self.contents)):
    #             user = random.choice(self.terrestrial.mobiles)
    #             self.terrestrial.content_request(user, self.contents[i])
    #
    #         self_hits.append(self.terrestrial.self_hit / len(self.contents))
    #         d2d_hits.append(self.terrestrial.d2d_hit / len(self.contents))
    #         bs_hits.append(self.terrestrial.es_hit / len(self.contents))
    #         universal.append(self.terrestrial.miss / len(self.contents))
    #         self.terrestrial.clear_caches()
    #
    #     return self_hits, d2d_hits, bs_hits,  universal


    def simulate_DRL(self):
        # 进行格式化
        self.terrestrial.clear_caches()

        self.terrestrial.edge_sever.set_cache(EDGE_SEVER_CACHE_CAPACITY, "DRL")

        for mobile in self.terrestrial.mobiles:
            mobile.set_cache(MOBILE_CACHE_CAPACITY, "DRL")

        self.request_contents_randomly()
        self.print_cache_stats("DRL")



    def simulate(self):
        self.simulate_DRL()
