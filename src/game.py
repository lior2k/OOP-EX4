from GraphAlgo import GraphAlgo
from agent import Agent
from pokemon import Pokemon
EPSILON = 0.01


class Game:

    def __init__(self, algo: GraphAlgo):
        self.pokemon_list: [Pokemon] = []
        self.agent_list = []
        self.Algo = algo

    def get_pokemons(self) -> [Pokemon]:
        return self.pokemon_list

    def get_agents(self) -> [Agent]:
        return self.agent_list

    def get_agent(self, id: int):
        for agent in self.agent_list:
            if agent.get_id() == id:
                return agent
        return None

    def add_new_pokemon(self, pokemon: Pokemon) -> bool:
        for p in self.pokemon_list:
            if p == pokemon:
                return False
        self.pokemon_list.append(pokemon)
        self.set_src_and_dest(pokemon)
        return True

    def add_agents(self, agent: Agent):
        self.agent_list.append(agent)

    # def remove_done_pokemon(self, pokemon: Pokemon):
    #     self.pokemon_list.remove(pokemon)

    # remove caught pokemons from self(game) and also every agent
    def remove_caught(self, current_active_pokemons: [Pokemon]):
        for p in self.pokemon_list:
            flag = 1
            for p2 in current_active_pokemons:
                if p == p2:
                    flag = 0
            if flag == 1:
                for agent in self.agent_list:
                    if agent.get_pokemon_list().__contains__(p):
                        agent.get_pokemon_list().remove(p)
                self.pokemon_list.remove(p)

    # return fastest available agent if exists
    def get_fastest_free_agent(self):
        speed = -1
        a1 = None
        for agent in self.agent_list:
            if agent.get_state() == 0:
                if agent.get_speed() > speed:
                    speed = agent.get_speed()
                    a1 = agent
        return a1

    # set the pokemon's src and dest fields to his edge corresponding src and dest
    def set_src_and_dest(self, pokemon: Pokemon):
        for n1 in self.Algo.get_graph().get_all_v().values():
            for n2 in self.Algo.get_graph().get_all_v().values():
                if n1 is not n2:
                    if self.is_pokemon_between_nodes(pokemon, n1.get_pos(), n2.get_pos()):
                        if pokemon.get_type() > 0:
                            if n1.get_id() < n2.get_id():
                                pokemon.set_src_node(n1)
                                pokemon.set_dest_node(n2)
                            else:
                                pokemon.set_src_node(n2)
                                pokemon.set_dest_node(n1)
                        else:
                            if n1.get_id() < n2.get_id():
                                pokemon.set_src_node(n2)
                                pokemon.set_dest_node(n1)
                            else:
                                pokemon.set_src_node(n1)
                                pokemon.set_dest_node(n2)

    # check if the edge between two nodes contains the pokemon
    def is_pokemon_between_nodes(self, pokemon: Pokemon, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = self.get_scaled_xy((pos1[0], pos1[1]))
        x2, y2 = self.get_scaled_xy((pos2[0], pos2[1]))
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return abs(pokemon.get_pos()[1] - (a * pokemon.get_pos()[0] + b)) < EPSILON

    def get_scaled_xy(self, coordinates: tuple) -> ():
        width, height = 1080, 720
        wide_factor = width / (self.Algo.graph.max_x - self.Algo.graph.min_x)
        height_factor = height / (self.Algo.graph.max_y - self.Algo.graph.min_y)
        x = (((coordinates[0] - self.Algo.graph.min_x) * wide_factor) * 0.65) + 150
        y = (((coordinates[1] - self.Algo.graph.min_y) * height_factor) * 0.65) + 100
        return x, y

    def update_agent(self, agent: Agent):
        a1 = self.get_agent(agent.id)
        a1.set_pos(agent.get_pos())
        a1.set_value(agent.get_value())
        a1.set_speed(agent.get_speed())
        a1.set_src_index(agent.get_src_index())
        a1.set_dest_index(agent.get_dest_index())

