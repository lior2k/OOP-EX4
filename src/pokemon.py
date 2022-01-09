from src.mynode import MyNode


class Pokemon:

    # state: 0 = init, 1 = agent on the way, 2 = done
    def __init__(self, weight: int = None, type: int = None, pos: (float, float, float) = None):
        self.weight = weight
        self.type = type
        self.pos = pos
        self.src_node = None
        self.dest_node = None
        self.state = 0

    def get_type(self) -> int:
        return self.type

    def get_weight(self) -> int:
        return self.weight

    def get_pos(self) -> tuple:
        return self.pos

    def get_state(self) -> int:
        return self.state

    def set_state(self, state: int):
        self.state = state

    def get_src_node(self) -> MyNode:
        return self.src_node

    def set_src_node(self, node: MyNode):
        self.src_node = node

    def get_dest_node(self) -> MyNode:
        return self.dest_node

    def set_dest_node(self, node: MyNode):
        self.dest_node = node

    # def __str__(self):
    #     return f"w: {self.weight}, t: {self.type}, p: {self.pos}, state: {self.state}"
    #
    # def __repr__(self):
    #     return f"w: {self.weight}, t: {self.type}, p: {self.pos}, state: {self.state}"

    def __str__(self):
        return f"src index: {self.get_src_node().get_id()}, dest_index: {self.get_dest_node().get_id()}, p: {self.pos}"

    def __repr__(self):
        return f"src index: {self.get_src_node().get_id()}, dest_index: {self.get_dest_node().get_id()}, p: {self.pos}"

    def __eq__(self, other):
        if isinstance(other, Pokemon):
            if other.pos == self.pos and other.type == self.type and other.weight == self.weight:
                return True
        return False
