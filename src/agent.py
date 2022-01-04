from src.mynode import MyNode
from src.pokemon import Pokemon


class Agent:

    # state: 0 = level, 1 = on way
    def __init__(self, id: int, val: float,  speed: float, src: int = None, dest: int = None, pos: tuple = None):
        self.id = id
        self.value = val
        self.src_index = src
        self.dest_index = dest
        self.speed = speed
        self.pos = pos
        self.current_path: [int] = []
        self.state = 0
        self.pokemons: [Pokemon] = []
        # self.dest_node = None

    def get_id(self) -> int:
        return self.id

    def get_value(self) -> float:
        return self.value

    def set_value(self, value: float):
        self.value = value

    def get_src_index(self) -> int:
        return self.src_index

    def set_src_index(self, src: int):
        self.src_index = src

    def get_dest_index(self) -> int:
        return self.dest_index

    def set_dest_index(self, dest: int):
        self.dest_index = dest

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, speed: float):
        self.speed = speed

    def get_pos(self) -> tuple:
        return self.pos

    def set_pos(self, pos: tuple):
        self.pos = pos

    def get_curr_path(self) -> [int]:
        return self.current_path

    def get_state(self):
        return self.state

    def set_state(self, state: int):
        self.state = state

    def get_dest_node(self):
        return self.dest_node

    def set_dest_node(self, node: MyNode):
        self.dest_node = node

    def get_pokemon_list(self):
        return self.pokemons

    def add_pokemon_to_list(self, pokemon: Pokemon):
        self.pokemons.append(pokemon)

    # def clear_pokemons(self):
    #     for p in self.pokemons:
    #         pdest_node = p.get_dest_node()
    #         if self.dest_node == pdest_node:
    #             self.pokemons.remove(p)

    def add_path(self, ids: [int]):
        for id in ids:
            self.current_path.append(id)

    # def __str__(self):
    #     return f"id: {self.id}, val: {self.value}, speed: {self.speed}, src: {self.src}. dest: {self.dest}"
    #
    # def __repr__(self):
    #     return f"id: {self.id}, val: {self.value}, speed: {self.speed}, src: {self.src}. dest: {self.dest}"

    def __str__(self):
        return f"id: {self.id}, path: {self.current_path}, dest: {self.dest_index}, pos: {self.pos}"

    def __repr__(self):
        return f"id: {self.id}, path: {self.current_path}, dest: {self.dest_index}, pos: {self.pos}"
