import json
import math
from types import SimpleNamespace
import pygame
from src.GraphAlgo import GraphAlgo
from src.agent import Agent
from src.pokemon import Pokemon
from src.client import Client

EPSILON = 0.01


class Game:

    def __init__(self, algo: GraphAlgo, win: pygame.Surface):
        self.pokemon_list: [Pokemon] = []
        self.agent_list = []
        self.Algo = algo
        self.win = win

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

    def choose_best_agent(self, pokemon: Pokemon) -> (Agent, float, [int]):
        best_agent = None
        best_cost = math.inf
        best_path = []
        best_dist = -1
        src_node = pokemon.get_src_node()
        dest_node = pokemon.get_dest_node()

        for agent in self.agent_list:

            poke_len = len(agent.get_pokemon_list())
            if agent.get_dest_index() == -1:
                agent_pos = agent.get_src_index()
            else:
                agent_pos = agent.get_dest_index()

            if poke_len == 0:
                dist, path = self.Algo.shortest_path(agent_pos, src_node.get_id())
                dist = dist + self.Algo.get_graph().all_out_edges_of_node(src_node.get_id())[dest_node.get_id()]
                path.append(dest_node.get_id())
                cost = dist / agent.get_speed()
                if cost < best_cost:
                    best_cost = cost
                    best_agent = agent
                    best_dist = dist
                    best_path = path
            elif poke_len >= 1:
                p2 = agent.get_pokemon_list()[0]

                # from agent to p2 to new pokemon
                dist0, path0 = self.Algo.shortest_path(agent_pos, p2.get_src_node().get_id())
                dist0 = dist0 + self.Algo.get_graph().all_out_edges_of_node(p2.get_src_node().get_id())[
                    p2.get_dest_node().get_id()]
                dist1, path1 = self.Algo.shortest_path(p2.get_dest_node().get_id(), src_node.get_id())
                dist1 = dist1 + self.Algo.get_graph().all_out_edges_of_node(src_node.get_id())[dest_node.get_id()]
                path1.append(pokemon.get_dest_node().get_id())
                cost1 = (agent.dist + dist1) / agent.get_speed()

                # from agent to new pokemon to p2
                dist2, path2 = self.Algo.shortest_path(agent_pos, src_node.get_id())
                dist2 = dist2 + self.Algo.get_graph().all_out_edges_of_node(src_node.get_id())[dest_node.get_id()]
                dist3, path3 = self.Algo.shortest_path(dest_node.get_id(), p2.get_src_node().get_id())
                dist3 = dist3 + self.Algo.get_graph().all_out_edges_of_node(p2.get_src_node().get_id())[
                    p2.get_dest_node().get_id()]
                path3.append(p2.get_dest_node().get_id())
                cost2 = (dist2 + dist3) / agent.get_speed()

                if cost1 < cost2 and cost1 < best_cost:
                    best_cost = cost1
                    best_agent = agent
                    best_dist = dist0 + dist1
                    i = 0
                    while i < len(path1):
                        path0.append(path1[i])
                        i += 1
                    best_path = path0
                elif cost2 < cost1 and cost2 < best_cost:
                    best_cost = cost2
                    i = 0
                    while i < len(path3):
                        path2.append(path3[i])
                        i += 1
                    best_agent = agent
                    best_dist = dist2 + dist3
                    best_path = path2

        return best_agent, best_dist, best_path

    def on_way(self, pokemon: Pokemon) -> bool:
        src = pokemon.get_src_node().get_id()
        dest = pokemon.get_dest_node().get_id()
        for agent in self.agent_list:
            index = 0
            path = agent.get_curr_path()
            while index < len(path)-1:
                if path[index] == src:
                    if path[index+1] == dest:
                        pokemon.set_state(1)
                        return True
                index += 1
        return False

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

    def is_pokemon_between_nodes(self, pokemon: Pokemon, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = self.get_scaled_xy((pos1[0], pos1[1]))
        x2, y2 = self.get_scaled_xy((pos2[0], pos2[1]))
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return abs(pokemon.get_pos()[1] - (a * pokemon.get_pos()[0] + b)) < EPSILON

    def get_scaled_xy(self, coordinates: tuple) -> ():
        wide_factor = self.win.get_width() / (self.Algo.graph.max_x - self.Algo.graph.min_x)
        height_factor = self.win.get_height() / (self.Algo.graph.max_y - self.Algo.graph.min_y)
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

    def load_agents(self, client: Client, gui):
        agents_str = json.loads(client.get_agents(),
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [A.Agent for A in agents_str]
        for A in agents:
            x_str, y_str, _ = A.pos.split(',')
            x, y = gui.get_scaled_xy((float(x_str), float(y_str)))
            agent = Agent(A.id, A.value, A.speed, A.src, A.dest, (x, y))
            self.add_agents(agent)

    def add_initial_agents(self, client: Client, gui):
        pokemon_list = []
        dict_info = json.loads(client.get_info())
        info = dict_info['GameServer']
        num_of_agents = info['agents']
        pokemons_str = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons_str]
        for p in pokemons:
            x_str, y_str, _ = p.pos.split(',')
            x, y = gui.get_scaled_xy((float(x_str), float(y_str)))
            new_pokemon = Pokemon(p.value, p.type, (x, y))
            pokemon_list.append(new_pokemon)

        pokemon_list.sort(key=Pokemon.get_weight, reverse=True)

        if num_of_agents == 1:
            self.set_src_and_dest(pokemon_list[0])
            src = pokemon_list[0].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
        elif num_of_agents == 2:
            self.set_src_and_dest(pokemon_list[0])
            src = pokemon_list[0].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
            self.set_src_and_dest(pokemon_list[1])
            src = pokemon_list[1].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
        elif num_of_agents == 3:
            self.set_src_and_dest(pokemon_list[0])
            src = pokemon_list[0].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
            self.set_src_and_dest(pokemon_list[1])
            src = pokemon_list[1].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
            self.set_src_and_dest(pokemon_list[2])
            src = pokemon_list[2].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
        elif num_of_agents == 4:
            self.set_src_and_dest(pokemon_list[0])
            src = pokemon_list[0].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
            self.set_src_and_dest(pokemon_list[1])
            src = pokemon_list[1].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
            self.set_src_and_dest(pokemon_list[2])
            src = pokemon_list[2].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")
            self.set_src_and_dest(pokemon_list[3])
            src = pokemon_list[3].get_src_node().get_id()
            client.add_agent("{\"id\":" + str(src) + "}")

