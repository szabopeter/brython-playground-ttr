import unittest
from player import Player
from playercontrol import PlayerControl
from gameconfig import game_config
from testutil import BrythonFunctionsMock


USE_MOCK = False

def create_control():
    if USE_MOCK:
        from unittest.mock import Mock
        return Mock()

    brython_functions = BrythonFunctionsMock.accepting_anything()
    return PlayerControl(0, game_config, brython_functions)


class PlayerTestCase(unittest.TestCase):
    def test_creation(self):
        p = Player(2, None)
        self.assertEqual(p.total_score, 0)

    def test_scoring(self):
        p = Player(2, create_control())
        p.update_count(5, 3)
        p.update_ticket_score(8)
        self.assertEqual(p.total_score, 3 * 10 + 8)

    def test_disallow_negative_count(self):
        p = Player(2, create_control())
        p.decrease_count(4)
        self.assertEqual(p.total_score, 0)

    def test_longest_road_scoring(self):
        p = Player(3, create_control())

        p.set_longest_road(True)
        self.assertEqual(p.total_score, 10)

        p.set_longest_road(False)
        self.assertEqual(p.total_score, 0)


if __name__ == '__main__':
    unittest.main()
