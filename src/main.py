import json
import time
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


def load_and_draw():
    bg = pygame.image.load("field_bg.jpeg")
    win.blit(bg, (0, 0))
    draw_text()
    Algo.draw_graph(win)
    draw_agents()
    load_and_draw_pokemons()
    if 50 < pos[0] < 150 and 50 < pos[1] < 100:
        draw_button(1)
    else:
        draw_button()


def pygame_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 50 < pos[0] < 150 and 50 < pos[1] < 100:
                client.stop_connection()


def add_initial_agents():
    pokemon_list = []
    dict_info = json.loads(client.get_info())
    info = dict_info['GameServer']
    num_of_agents = info['agents']
    pokemons_str = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons_str]
    for p in pokemons:
        x_str, y_str, _ = p.pos.split(',')
        x, y = get_scaled_xy((float(x_str), float(y_str)))
        new_pokemon = Pokemon(p.value, p.type, (x, y))
        pokemon_list.append(new_pokemon)

    pokemon_list.sort(key=Pokemon.get_weight, reverse=True)

    if num_of_agents == 1:
        game.set_src_and_dest(pokemon_list[0])
        src = pokemon_list[0].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
    elif num_of_agents == 2:
        game.set_src_and_dest(pokemon_list[0])
        src = pokemon_list[0].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
        game.set_src_and_dest(pokemon_list[1])
        src = pokemon_list[1].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
    elif num_of_agents == 3:
        game.set_src_and_dest(pokemon_list[0])
        src = pokemon_list[0].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
        game.set_src_and_dest(pokemon_list[1])
        src = pokemon_list[1].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
        game.set_src_and_dest(pokemon_list[2])
        src = pokemon_list[2].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
    elif num_of_agents == 4:
        game.set_src_and_dest(pokemon_list[0])
        src = pokemon_list[0].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
        game.set_src_and_dest(pokemon_list[1])
        src = pokemon_list[1].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
        game.set_src_and_dest(pokemon_list[2])
        src = pokemon_list[2].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")
        game.set_src_and_dest(pokemon_list[3])
        src = pokemon_list[3].get_src_node().get_id()
        client.add_agent("{\"id\":" + str(src) + "}")


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
        new_pokemon = Pokemon(p.value, p.type, (x, y))
        pokemon_list.append(new_pokemon)
        game.add_new_pokemon(new_pokemon)

        # draw the pokemon weight
        font = pygame.font.SysFont('Arial', 15)
        weight_str = str(new_pokemon.get_weight())
        text = font.render(weight_str, True, (255, 0, 0))
        pokemon_pic = pygame.image.load("pokemon2525.png")
        win.blit(pokemon_pic, (int(x), int(y)))
        rect = text.get_rect(center=(new_pokemon.get_pos()[0]-15, new_pokemon.get_pos()[1]-15))
        win.blit(text, rect)

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

        # draw agent and agent id
        font = pygame.font.SysFont('Arial', 15)
        t1 = font.render(str(A.id), True, (0, 0, 0))
        agent_pic = pygame.image.load("agent3030.png")
        win.blit(agent_pic, (int(x), int(y)))
        rect = t1.get_rect(center=((int(x)), int(y)))
        win.blit(t1, rect)


def draw_text():
    font = pygame.font.SysFont('Arial', 20)
    info = info_dict['GameServer']
    moves_str = "moves: " + str(info['moves'])
    grade_str = "grade: " + str(info['grade'])
    level_str = "level: " + str(info['game_level'])
    time_in_ms = client.time_to_end()
    time_in_sec = int(int(time_in_ms) / 1000)
    time_str = "timer: " + str(time_in_sec)
    t1 = font.render(moves_str, True, (0, 0, 0))
    t2 = font.render(grade_str, True, (0, 0, 0))
    t3 = font.render(level_str, True, (0, 0, 0))
    t4 = font.render(time_str, True, (0, 0, 0))
    rect = t1.get_rect(center=(win.get_width()/2 - 200, 20))
    win.blit(t1, rect)
    rect = t2.get_rect(center=(win.get_width()/2 - 100, 20))
    win.blit(t2, rect)
    rect = t3.get_rect(center=(win.get_width()/2, 20))
    win.blit(t3, rect)
    rect = t4.get_rect(center=(win.get_width()/2 + 100, 20))
    win.blit(t4, rect)


def draw_button(flag: int = 0):
    font = pygame.font.SysFont('Arial', 30)
    if flag == 0:
        stop_button = font.render('stop', True, (200, 200, 200))
        rect = stop_button.get_rect(center=(100, 70))
        pygame.draw.rect(win, (0, 0, 0), (50, 50, 100, 50))
        win.blit(stop_button, rect)
    elif flag == 1:
        stop_button = font.render('stop', True, (200, 200, 200))
        rect = stop_button.get_rect(center=(100, 70))
        pygame.draw.rect(win, (255, 0, 0), (50, 50, 100, 50))
        win.blit(stop_button, rect)


if __name__ == '__main__':
    client = start_client()
    Algo = load_graph_and_algo(client)

    total_moves = 0

    width, height = 1080, 889
    win = pygame.display.set_mode((width, height), depth=32, flags=RESIZABLE)
    pygame.font.init()
    game = Game(Algo, win)
    add_initial_agents()
    load_agents()

    pygame.display.set_caption("Pokemon Game")

    client.start()
    total_time = int(client.time_to_end())/1000
    clock = pygame.time.Clock()

    while client.is_running() == 'true':
        clock.tick(60)

        info_dict = json.loads(client.get_info())

        pos = pygame.mouse.get_pos()
        load_and_draw()
        pygame_loop()

        # assign agents to pokemons
        for pokemon in game.pokemon_list:
            if pokemon.get_state() == ON_WAY:
                continue
            elif pokemon.get_state() == INIT:
                # on_way = game.on_way(pokemon)
                # if not on_way:
                game.choose_best_agent(pokemon)

        # send agents
        for agent in game.get_agents():
            # print(agent.get_id(), agent.get_curr_path(), agent.get_pokemon_list())
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
        time.sleep(0.01)
