import unittest
from unittest.mock import Mock
from player import Player


class PlayerMock:
    def __init__(self, nr, control=None):
        self.nr = nr
        self.control = PlayerControlMock(nr) if control is None else control
        self.has_refreshed = False

    def update_all(self):
        self.has_refreshed = True


class PlayerControlMock:
    def __init__(self, nr):
        self.nr = nr


player_count = 5
default_controls = [PlayerControlMock(nr) for nr in range(player_count)]


class PlayerList:
    def __init__(self, players):
        self.players = players[:]

    def __len__(self):
        return len(self.players)

    def get_players(self):
        return self.players

    def move_to_last(self, player):
        controls = [p.control for p in self.players]
        self.players.remove(player)
        self.players.append(player)
        for i in range(len(controls)):
            player = self.players[i]
            if player.control != controls[i]:
                player.control = controls[i]
                player.update_all()


class PlayerListTestCase(unittest.TestCase):
    def assert_order(self, playerlist, expected_nrs):
        actual_nrs = [player.nr for player in playerlist.get_players()]
        self.assertSequenceEqual(actual_nrs, expected_nrs)

        control_nrs = [player.control.nr for player in playerlist.get_players()]
        self.assertSequenceEqual(control_nrs, list(range(len(playerlist))))

    def assert_has_refreshed(self, playerlist, expected_refresh):
        actual_refresh = [player.has_refreshed for player in playerlist.get_players()]
        self.assertSequenceEqual(actual_refresh, expected_refresh)

    def test_minimize_moves_to_last(self):
        players = [PlayerMock(nr, default_controls[nr]) for nr in range(player_count)]
        pl = PlayerList(players)
        pl.move_to_last(players[2])
        self.assert_order(pl, (0, 1, 3, 4, 2))
        self.assert_has_refreshed(pl, (False, False, True, True, True))
