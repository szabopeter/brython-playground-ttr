import unittest
from unittest.mock import Mock
from player import Player


class PlayerTestCase(unittest.TestCase):
    def test_creation(self):
        p = Player(2, None)
        self.assertEqual(p.total_score, 0)

    def test_scoring(self):
        p = Player(2, Mock())
        p.update_count(5, 3)
        p.update_ticket_score(8)
        self.assertEqual(p.total_score, 3 * 10 + 8)

    def test_disallow_negative_count(self):
        p = Player(2, None)
        p.decrease_count(4)
        self.assertEqual(p.total_score, 0)

    def test_longest_road_scoring(self):
        p = Player(3, Mock())

        p.set_longest_road(True)
        self.assertEqual(p.total_score, 10)

        p.set_longest_road(False)
        self.assertEqual(p.total_score, 0)


if __name__ == '__main__':
    unittest.main()
