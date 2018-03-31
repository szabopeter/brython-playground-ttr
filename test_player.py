import unittest
from unittest.mock import Mock
from player import Player


class PlayerTestCase(unittest.TestCase):
    def test_creation(self):
        p = Player(2, None)
        self.assertEqual(p.total_score, 0)

    def test_scoring(self):
        pc = Mock()
        p = Player(2, pc)
        p.update_count(5, 3)
        p.update_ticket_score(8)
        self.assertEqual(p.total_score, 3 * 10 + 8)


if __name__ == '__main__':
    unittest.main()
