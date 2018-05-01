import unittest

from player import Player
from testutil import create_player_control_mock


class PlayerTestCase(unittest.TestCase):
    def test_creation(self):
        p = Player(2, None)
        self.assertEqual(p.total_score, 0)

    def test_scoring(self):
        p = Player(2, create_player_control_mock())
        p.update_count(5, 3)
        p.update_ticket_score(8)
        self.assertEqual(p.total_score, 3 * 10 + 8)

    def test_disallow_negative_count(self):
        p = Player(2, create_player_control_mock())
        p.decrease_count(4)
        self.assertEqual(p.total_score, 0)

    def test_longest_road_scoring(self):
        p = Player(3, create_player_control_mock())

        p.set_longest_road(True)
        self.assertEqual(p.total_score, 10)

        p.set_longest_road(False)
        self.assertEqual(p.total_score, 0)

    def test_serialization(self):
        player = Player(2, create_player_control_mock())
        player.update_count(5, 3)
        serializable = player.serializeable()
        clone = Player.from_serializeable(serializable)
        self.assertEqual(player, clone)
        self.assertEqual(player.counts, clone.counts)
        self.assertEqual(player.total_score, clone.total_score)


if __name__ == '__main__':
    unittest.main()
