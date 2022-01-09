from unittest import TestCase
import pygame.display
from src.GraphAlgo import GraphAlgo
from src.agent import Agent
from src.game import Game
from src.mynode import MyNode
from src.pokemon import Pokemon

Algo = GraphAlgo()
Algo.load_from_json('A5.json')
n1 = MyNode(88, (35.20154022114608, 32.10594485882353, 0.0))
n2 = MyNode(99, (35.19805902663438, 32.10525428067227, 0.0))
Algo.graph.add_mynode(n1)
Algo.graph.add_mynode(n2)
Algo.get_graph().add_edge(99, 88, 2)
Algo.get_graph().add_edge(88, 99, 2)
win = pygame.display.set_mode((800, 659))
a1 = Agent(0, 0, 1.0, 0, -1, (0, 0, 0))
p1 = Pokemon(3, -1, (32.1, 34.8, 0))
p1.set_state(1)
game = Game(Algo, win)
p = Pokemon(5, -1, (35.19805902663438, 32.10525428067227))
game.add_new_pokemon(p)
game.agent_list.append(a1)
game.pokemon_list.append(p1)


class TestGame(TestCase):
    def test_get_pokemons(self):
        self.assertEqual(game.get_pokemons()[0], p1)

    def test_get_agents(self):
        self.assertEqual(game.get_agents()[0], a1)

    def test_get_agent(self):
        self.assertEqual(game.get_agent(0), a1)

    def test_add_new_pokemon(self):
        p2 = Pokemon(4, -1, (32.2, 35.1, 0))
        game.add_new_pokemon(p2)
        self.assertEqual(game.get_pokemons()[1], p2)
        p3 = Pokemon(3, -1, (32.1, 34.8, 0))
        self.assertTrue(not game.add_new_pokemon(p3))

    def test_add_agents(self):
        a2 = Agent(1, 0, 1.0, 0, -1, (0, 0, 0))
        game.add_agents(a2)
        self.assertEqual(game.agent_list[1], a2)

    # client dependent
    # def test_set_src_and_dest(self):
    #     self.assertEqual(p.get_src_node().get_id(), 99)
    #     self.assertEqual(p.get_dest_node().get_id(), 88)
    # def test_is_pokemon_between_nodes(self):
    #     self.assertTrue(game.is_pokemon_between_nodes(p, n1.get_pos(), n2.get_pos()))
    # def test_choose_best_agent(self):
    #     self.fail()
    # def test_on_way(self):
    #     self.fail()
    # def test_remove_caught(self):
    #     self.fail()
    # def test_update_agent(self):
    #     self.fail()
    # def test_load_agents(self):
    #     self.fail()
    # def test_add_initial_agents(self):
    #     self.fail()
