import json
from types import SimpleNamespace

import pygame
from pygame import *
from pygame import gfxdraw

from src import GraphAlgo
from src.agent import Agent
from src.client import Client
from src.game import Game
from src.pokemon import Pokemon


class GUI:

    def __init__(self, client: Client, Algo: GraphAlgo):
        self.width, self.height = 800, 659
        self.client = client
        self.win = pygame.display.set_mode((self.width, self.height), depth=32, flags=RESIZABLE)
        pygame.font.init()
        pygame.display.set_caption("Pokemon Game")
        self.Algo = Algo

    def load_and_draw(self, game: Game):
        pos = pygame.mouse.get_pos()
        bg = pygame.image.load("images/field_bg.jpeg")
        self.win.blit(bg, (0, 0))
        self.draw_text()
        self.draw_graph()
        self.draw_agents(game)
        self.load_and_draw_pokemons(game)
        if 50 < pos[0] < 150 and 50 < pos[1] < 100:
            self.draw_button(1)
        else:
            self.draw_button()

    def pygame_loop(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 50 < pos[0] < 150 and 50 < pos[1] < 100:
                    self.client.stop_connection()
                    exit(0)

    def draw_agents(self, game: Game):
        agent_list = []
        agents_str = json.loads(self.client.get_agents(),
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [A.Agent for A in agents_str]
        for A in agents:
            x_str, y_str, _ = A.pos.split(',')
            x, y = self.get_scaled_xy((float(x_str), float(y_str)))
            game.get_agent(A.id).set_pos((x, y))
            agent = Agent(A.id, A.value, A.speed, A.src, A.dest, (x, y))
            game.update_agent(agent)
            agent_list.append(agent)

            # draw agent and agent id
            font = pygame.font.SysFont('Arial', 15)
            t1 = font.render(str(A.id), True, (0, 0, 0))
            agent_pic = pygame.image.load("images/agent3030.png")
            self.win.blit(agent_pic, (int(x), int(y)))
            rect = t1.get_rect(center=((int(x)), int(y)))
            self.win.blit(t1, rect)

    def draw_text(self):
        info_dict = json.loads(self.client.get_info())
        font = pygame.font.SysFont('Arial', 20)
        info = info_dict['GameServer']
        moves_str = "moves: " + str(info['moves'])
        grade_str = "grade: " + str(info['grade'])
        level_str = "level: " + str(info['game_level'])
        time_in_ms = self.client.time_to_end()
        time_in_sec = int(int(time_in_ms) / 1000)
        time_str = "timer: " + str(time_in_sec)
        t1 = font.render(moves_str, True, (0, 0, 0))
        t2 = font.render(grade_str, True, (0, 0, 0))
        t3 = font.render(level_str, True, (0, 0, 0))
        t4 = font.render(time_str, True, (0, 0, 0))
        rect = t1.get_rect(center=(self.win.get_width() / 2 - 200, 20))
        self.win.blit(t1, rect)
        rect = t2.get_rect(center=(self.win.get_width() / 2 - 100, 20))
        self.win.blit(t2, rect)
        rect = t3.get_rect(center=(self.win.get_width() / 2, 20))
        self.win.blit(t3, rect)
        rect = t4.get_rect(center=(self.win.get_width() / 2 + 100, 20))
        self.win.blit(t4, rect)

    def draw_graph(self):
        radius = 15
        for node in self.Algo.graph.get_all_v().values():
            x = node.get_pos()[0]
            y = node.get_pos()[1]
            scaled_x, scaled_y = self.get_scaled_xy((x, y))
            gfxdraw.filled_circle(self.win, int(scaled_x), int(scaled_y), radius, node.get_tag())
            gfxdraw.aacircle(self.win, int(scaled_x), int(scaled_y), radius, (255, 255, 255))
            pos = str(node.get_id())
            font = pygame.font.SysFont('Arial', 20)
            text = font.render(pos, True, (255, 255, 255))
            rect = text.get_rect(center=(scaled_x, scaled_y))
            self.win.blit(text, rect)
            for dest_index in node.get_out_edges():
                dest_x = self.Algo.get_graph().get_all_v()[dest_index].get_pos()[0]
                dest_y = self.Algo.get_graph().get_all_v()[dest_index].get_pos()[1]
                scaled_xd, scaled_yd = self.get_scaled_xy((dest_x, dest_y))
                pygame.draw.line(self.win, (61, 72, 126), (scaled_x, scaled_y), (scaled_xd, scaled_yd))
                # self.draw_arrow_head(win, x, y, dest_x, dest_y)

    def draw_button(self, flag: int = 0):
        font = pygame.font.SysFont('Arial', 30)
        if flag == 0:
            stop_button = font.render('stop', True, (200, 200, 200))
            rect = stop_button.get_rect(center=(100, 70))
            pygame.draw.rect(self.win, (0, 0, 0), (50, 50, 100, 50))
            self.win.blit(stop_button, rect)
        elif flag == 1:
            stop_button = font.render('stop', True, (200, 200, 200))
            rect = stop_button.get_rect(center=(100, 70))
            pygame.draw.rect(self.win, (255, 0, 0), (50, 50, 100, 50))
            self.win.blit(stop_button, rect)

    def load_and_draw_pokemons(self, game: Game) -> None:
        pokemon_list = []
        pokemons_str = json.loads(self.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons_str]
        for p in pokemons:
            x_str, y_str, _ = p.pos.split(',')
            x, y = self.get_scaled_xy((float(x_str), float(y_str)))
            new_pokemon = Pokemon(p.value, p.type, (x, y))
            pokemon_list.append(new_pokemon)
            game.add_new_pokemon(new_pokemon)

            # draw the pokemon weight
            font = pygame.font.SysFont('Arial', 15)
            weight_str = str(new_pokemon.get_weight())
            text = font.render(weight_str, True, (255, 0, 0))
            pokemon_pic = pygame.image.load("images/pokemon2525.png")
            self.win.blit(pokemon_pic, (int(x), int(y)))
            rect = text.get_rect(center=(new_pokemon.get_pos()[0] - 15, new_pokemon.get_pos()[1] - 15))
            self.win.blit(text, rect)

        # remove caught pokemons from game&agents
        game.remove_caught(pokemon_list)

    def get_scaled_xy(self, coordinates: ()) -> ():
        wide_factor = self.win.get_width() / (self.Algo.graph.max_x - self.Algo.graph.min_x)
        height_factor = self.win.get_height() / (self.Algo.graph.max_y - self.Algo.graph.min_y)
        x = (((coordinates[0] - self.Algo.graph.min_x) * wide_factor) * 0.65) + 150
        y = (((coordinates[1] - self.Algo.graph.min_y) * height_factor) * 0.65) + 100
        return x, y