import json

import pygame

from GraphAlgo import GraphAlgo
from client import Client
from game import Game
from src.gui import GUI

INIT = 0
ON_WAY = 1
DONE = 2


def start_client():
    server_client = Client()
    port = 6666
    host = '127.0.0.1'
    server_client.start_connection(host, port)
    return server_client


def load_graph_and_algo():
    graph_json = client.get_graph()
    json_obj = json.loads(graph_json)
    with open('curr_graph', 'w') as f:
        json.dump(json_obj, f)
    graph_algo = GraphAlgo()
    graph_algo.load_from_json('curr_graph')
    return graph_algo


if __name__ == '__main__':
    client = start_client()
    Algo = load_graph_and_algo()

    total_moves = 0

    gui = GUI(client, Algo)
    game = Game(Algo, gui.win)
    game.add_initial_agents(client, gui)
    game.load_agents(client, gui)

    client.start()
    total_time = int(client.time_to_end())/1000
    clock = pygame.time.Clock()

    while client.is_running() == 'true':
        clock.tick(60)
        gui.load_and_draw(game)
        gui.pygame_loop()
        # assign agents to pokemons
        for pokemon in game.pokemon_list:
            if pokemon.get_state() == ON_WAY:
                continue
            elif pokemon.get_state() == INIT:
                on_way = game.on_way(pokemon)
                if not on_way:
                    agent, dist, path = game.choose_best_agent(pokemon)
                    agent.dist = dist
                    agent.current_path = path
                    agent.add_pokemon(pokemon)
                    agent.set_state(1)
                    pokemon.set_state(1)

        # send agents
        for agent in game.get_agents():
            if len(agent.get_curr_path()) > 0 and agent.get_dest_index() == -1:
                if agent.get_src_index() == agent.current_path[0]:
                    if agent.prev is not None and agent.prev != agent.get_src_index():
                        agent.dist = agent.dist - Algo.graph.all_out_edges_of_node(agent.prev)[agent.get_src_index()]
                    agent.prev = agent.get_src_index()
                    agent.get_curr_path().remove(agent.get_src_index())
                    if len(agent.get_curr_path()) == 0:
                        agent.dist = 0
                        agent.prev = None
                        agent.set_state(INIT)
                        continue
                client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(agent.get_curr_path()[0]) + '}')

        current_time = int(client.time_to_end())/1000
        if total_moves < (total_time - current_time) * 10:
            client.move()
            total_moves += 1

        pygame.display.update()
        # time.sleep(0.01)
