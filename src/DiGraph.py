import math
import random

from src.mynode import MyNode
from src.GraphInterface import GraphInterface
Max_Value = math.inf


class DiGraph(GraphInterface):

    def __init__(self):
        self.nodes_dict: {int, MyNode} = {}
        self.node_size = 0
        self.edge_size = 0
        self.mc = 0
        self.max_x = -1
        self.max_y = -1
        self.min_x = Max_Value
        self.min_y = Max_Value

    def v_size(self):
        return self.node_size

    def e_size(self):
        return self.edge_size

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 == id2:
            return False
        if self.nodes_dict.keys().__contains__(id1) and self.nodes_dict.keys().__contains__(id2):
            self.nodes_dict[id1].add_edge(id1, id2, weight)
            self.nodes_dict[id2].add_edge(id1, id2, weight)
            self.mc += 1
            self.edge_size += 1
            return True
        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.nodes_dict.keys().__contains__(node_id):
            return False
        if pos is None:
            x = random.random() * 800
            y = random.random() * 600
            pos = (x, y)
        if self.max_x < pos[0]:
            self.max_x = pos[0]
        if self.max_y < pos[1]:
            self.max_y = pos[1]
        if self.min_x > pos[0]:
            self.min_x = pos[0]
        if self.min_y > pos[1]:
            self.min_y = pos[1]
        n = MyNode(node_id, pos)
        self.nodes_dict[node_id] = n
        self.mc += 1
        self.node_size += 1
        return True

    def add_mynode(self, node: MyNode):
        self.nodes_dict[node.get_id()] = node

    def remove_node(self, node_id: int) -> bool:
        if self.nodes_dict.keys().__contains__(node_id):
            for dest in self.nodes_dict.get(node_id).get_out_edges():
                temp = self.nodes_dict[dest]
                temp.get_in_edges().pop(node_id)
            self.nodes_dict.pop(node_id)
            self.mc += 1
            self.node_size -= 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.nodes_dict.keys().__contains__(node_id1) and self.nodes_dict.keys().__contains__(node_id2):
            if self.nodes_dict.get(node_id1).get_out_edges().__contains__(node_id2) and self.nodes_dict.get(node_id2).get_in_edges().__contains__(node_id1):
                self.nodes_dict.get(node_id1).get_out_edges().pop(node_id2)
                self.nodes_dict.get(node_id2).get_in_edges().pop(node_id1)
                self.mc += 1
                self.edge_size -= 1
                return True
        return False

    def get_all_v(self) -> dict:
        return self.nodes_dict

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.nodes_dict[id1].get_in_edges()

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.nodes_dict[id1].get_out_edges()

    def __str__(self):
        return f"|V|={self.node_size} |E|={self.edge_size}"

    def get_max_x(self):
        return self.max_x

    def get_max_y(self):
        return self.max_y

    def get_min_x(self):
        return self.min_x

    def get_min_y(self):
        return self.min_y


