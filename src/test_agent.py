from unittest import TestCase

from src.agent import Agent
from src.pokemon import Pokemon

agent = Agent(0, 30, 11.1, 7, 8, (32.1, 34.8, 40))
pok = Pokemon(0)


class TestAgent(TestCase):

    def test_get_id(self):
        self.assertEqual(agent.get_id(), 0)

    def test_get_value(self):
        self.assertEqual(agent.get_value(), 30)

    def test_set_value(self):
        agent.set_value(35)
        self.assertEqual(agent.get_value(), 35)

    def test_get_src_index(self):
        self.assertEqual(agent.get_src_index(), 7)

    def test_set_src_index(self):
        agent.set_src_index(9)
        self.assertEqual(agent.get_src_index(), 9)

    def test_get_dest_index(self):
        self.assertEqual(agent.get_dest_index(), 8)

    def test_set_dest_index(self):
        agent.set_dest_index(10)
        self.assertEqual(agent.get_dest_index(), 10)

    def test_get_speed(self):
        self.assertEqual(agent.get_speed(), 11.1)

    def test_set_speed(self):
        agent.set_speed(15.6)
        self.assertEqual(agent.get_speed(), 15.6)

    def test_get_pos(self):
        self.assertEqual(agent.get_pos(), (32.1, 34.8, 40))

    def test_set_pos(self):
        pos = (22.1, 33.2, 70)
        agent.set_pos(pos)
        self.assertEqual(agent.get_pos(), pos)

    def test_get_curr_path(self):
        agent.current_path.clear()
        path_list = [1, 2, 7, 9, 12]
        agent.add_path(path_list)
        self.assertEqual(agent.get_curr_path(), path_list)

    def test_get_state(self):
        self.assertEqual(agent.get_state(), 0)

    def test_set_state(self):
        agent.set_state(1)
        self.assertEqual(agent.get_state(), 1)

    def test_get_pokemon_list(self):
        p1 = Pokemon(4, 1, (1, 2, 3))
        p2 = Pokemon(6, 1, (2, 1, 3))
        p3 = Pokemon(8, 1, (1, 3, 2))
        p4 = Pokemon(9, 1, (2, 3, 1))
        p5 = Pokemon(10, 1, (3, 2, 1))
        pok_list = [pok, p1, p2, p3, p4, p5]
        agent.add_pokemon(p1)
        agent.add_pokemon(p2)
        agent.add_pokemon(p3)
        agent.add_pokemon(p4)
        agent.add_pokemon(p5)
        i = 0
        for p in agent.get_pokemon_list():
            self.assertTrue(p.__eq__(pok_list[i]))
            i += 1

    def test_add_path(self):
        agent.current_path.clear()
        path_list2 = [7, 8, 6]
        agent.add_path(path_list2)
        self.assertEqual(agent.get_curr_path(), path_list2)

    def test_add_pokemon(self):

        agent.add_pokemon(pok)
        pok_list2 = agent.get_pokemon_list()
        self.assertTrue(pok.__eq__(pok_list2[len(pok_list2)-1]))
