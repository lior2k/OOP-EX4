import json
from types import SimpleNamespace

import pygame
from pygame import RESIZABLE

from agent import Agent
from client import Client
from GraphAlgo import GraphAlgo
from game import Game
from pokemon import Pokemon
INIT = 0
ON_WAY = 1
DONE = 2


def add_initial_agents():
    info_dict = json.loads(client.get_info())
    info = info_dict['GameServer']
    num_of_agents = info['agents']
    if num_of_agents == 1:
        client.add_agent("{\"id\":0}")
    elif num_of_agents == 2:
        client.add_agent("{\"id\":0}")
        client.add_agent("{\"id\":1}")
    elif num_of_agents == 3:
        client.add_agent("{\"id\":0}")
        client.add_agent("{\"id\":1}")
        client.add_agent("{\"id\":2}")
    elif num_of_agents == 4:
        client.add_agent("{\"id\":0}")
        client.add_agent("{\"id\":1}")
        client.add_agent("{\"id\":2}")
        client.add_agent("{\"id\":3}")


def start_client():
    server_client = Client()
    port = 6666
    host = '127.0.0.1'
    server_client.start_connection(host, port)
    return server_client


def get_scaled_xy(coordinates: ()) -> ():
    wide_factor = win.get_width() / (Algo.graph.max_x - Algo.graph.min_x)
    height_factor = win.get_height() / (Algo.graph.max_y - Algo.graph.min_y)
    x = (((coordinates[0] - Algo.graph.min_x) * wide_factor) * 0.65) + 150
    y = (((coordinates[1] - Algo.graph.min_y) * height_factor) * 0.65) + 100
    return x, y


def load_graph_and_algo(server_client: Client):
    graph_json = server_client.get_graph()
    json_obj = json.loads(graph_json)
    with open('curr_graph', 'w') as f:
        json.dump(json_obj, f)
    graph_algo = GraphAlgo()
    graph_algo.load_from_json('curr_graph')
    return graph_algo


def load_and_draw_pokemons() -> None:
    pokemon_list = []
    pokemons_str = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons_str]
    for p in pokemons:
        x_str, y_str, _ = p.pos.split(',')
        x, y = get_scaled_xy((float(x_str), float(y_str)))
        pokemon = Pokemon(p.value, p.type, (x, y))
        pokemon_list.append(pokemon)
        game.add_new_pokemon(pokemon)

        pygame.draw.circle(win, (0, 255, 255), (x, y), 10)

    # remove caught pokemons from game&agents
    game.remove_caught(pokemon_list)


def load_agents():
    agents_str = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [A.Agent for A in agents_str]
    for A in agents:
        x_str, y_str, _ = A.pos.split(',')
        x, y = get_scaled_xy((float(x_str), float(y_str)))
        agent = Agent(A.id, A.value, A.speed, A.src, A.dest, (x, y))
        game.add_agents(agent)


def draw_agents():
    agent_list = []
    agents_str = json.loads(client.get_agents(),
                            object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [A.Agent for A in agents_str]
    for A in agents:
        x_str, y_str, _ = A.pos.split(',')
        x, y = get_scaled_xy((float(x_str), float(y_str)))
        game.get_agent(A.id).set_pos((x, y))
        agent = Agent(A.id, A.value, A.speed, A.src, A.dest, (x, y))
        game.update_agent(agent)
        agent_list.append(agent)
    for agent in agent_list:
        pygame.draw.circle(win, (122, 61, 23), (int(agent.get_pos()[0]), int(agent.get_pos()[1])), 10)


if __name__ == '__main__':
    client = start_client()
    Algo = load_graph_and_algo(client)
    add_initial_agents()

    client.start()
    game = Game(Algo)
    width, height = 1080, 720
    win = pygame.display.set_mode((width, height), depth=32, flags=RESIZABLE)
    pygame.display.set_caption("Directed Weighted Graph")
    pygame.font.init()
    clock = pygame.time.Clock()
    load_agents()

    while client.is_running() == 'true':
        win.fill((0, 0, 0))
        Algo.draw_graph(win)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        load_and_draw_pokemons()
        draw_agents()


        # assign agents to pokemons
        for pokemon in game.pokemon_list:
            if pokemon.get_state() == ON_WAY:
                continue
            elif pokemon.get_state() == INIT:
                fastest_free_agent = game.get_fastest_free_agent()
                # closest_agent = game.get_closest_free_agent()
                # if closest free agent is faster then fastest agent pick closest
                if fastest_free_agent is not None:
                    pokemon.set_state(ON_WAY)
                    fastest_free_agent.set_state(ON_WAY)

                    dist, path = Algo.shortest_path(fastest_free_agent.get_src_index(), pokemon.get_src_node().get_id())
                    fastest_free_agent.add_pokemon_to_list(pokemon)
                    # fastest_free_agent.set_dest_node(pokemon.get_dest_node())
                    fastest_free_agent.add_path(path)
                    fastest_free_agent.current_path.append(pokemon.get_dest_node().get_id())
                # else:
                #

        # send agents
        for agent in game.get_agents():
            if len(agent.get_curr_path()) > 0:
                if agent.get_src_index() == agent.current_path[0]:
                    agent.get_curr_path().remove(agent.get_src_index())
                    if len(agent.get_curr_path()) == 0:
                        agent.set_state(INIT)
                        continue
                client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(agent.get_curr_path()[0]) + '}')

        ttl = client.time_to_end()
        print(ttl, client.get_info())
        client.move()
        pygame.display.update()


