from unittest import TestCase
from src.mynode import MyNode
from src.pokemon import Pokemon

pokemon = Pokemon(3, -1, (32.1, 34.8, 40))
pokemon.set_state(1)
pokemon.set_src_node(MyNode(0))
pokemon.set_dest_node(MyNode(10))


class TestPokemon(TestCase):

    def test_get_type(self):
        self.assertEqual(pokemon.get_type(), -1)

    def test_get_weight(self):
        self.assertEqual(pokemon.get_weight(), 3)

    def test_get_pos(self):
        self.assertEqual(pokemon.get_pos(), (32.1, 34.8, 40))

    def test_get_state(self):
        self.assertEqual(pokemon.get_state(), 1)

    def test_set_state(self):
        pokemon.set_state(0)
        self.assertEqual(pokemon.get_state(), 0)

    def test_get_src_node(self):
        self.assertEqual(pokemon.get_src_node().get_id(), 0)

    def test_set_src_node(self):
        pokemon.set_src_node(MyNode(3))
        self.assertEqual(pokemon.get_src_node().get_id(), 3)

    def test_get_dest_node(self):
        self.assertEqual(pokemon.get_dest_node().get_id(), 10)

    def test_set_dest_node(self):
        pokemon.set_dest_node(MyNode(12))
        self.assertEqual(pokemon.get_dest_node().get_id(), 12)
