import unittest

from playerlist import PlayerList


class PlayerMock:
    def __init__(self, nr, control=None):
        self.nr = nr
        self.control = PlayerControlMock(nr) if control is None else control
        self.has_refreshed = False
        self.is_minimized = False

    def update_all(self):
        self.has_refreshed = True

    def minimize(self):
        self.is_minimized = True

    def restore(self):
        self.is_minimized = False


class PlayerControlMock:
    def __init__(self, nr):
        self.nr = nr


player_count = 5
default_controls = [PlayerControlMock(nr) for nr in range(player_count)]


class PlayerListTestCase(unittest.TestCase):
    def assert_order(self, playerlist, expected_nrs):
        actual_nrs = [player.nr for player in playerlist.get_players()]
        self.assertSequenceEqual(actual_nrs, expected_nrs)

        control_nrs = [player.control.nr for player in playerlist.get_players()]
        self.assertSequenceEqual(control_nrs, list(range(len(playerlist))))

    def assert_has_refreshed(self, playerlist, expected_refresh):
        actual_refresh = [player.has_refreshed for player in playerlist.get_players()]
        self.assertSequenceEqual(actual_refresh, expected_refresh)

    def assert_is_minimized(self, playerlist, expected_is_minimized):
        actual_is_minimized = [player.is_minimized for player in playerlist.get_players()]
        self.assertSequenceEqual(actual_is_minimized, expected_is_minimized)

    def test_minimize_moves_to_last(self):
        players = [PlayerMock(nr, default_controls[nr]) for nr in range(player_count)]
        pl = PlayerList(players)
        pl.minimize_and_move_to_last(players[2])
        self.assert_order(pl, (0, 1, 3, 4, 2))
        self.assert_has_refreshed(pl, (False, False, True, True, True))
        self.assert_is_minimized(pl, (False, False, False, False, True))

    def test_restore_moves_up(self):
        players = [PlayerMock(nr, default_controls[nr]) for nr in range(player_count)]
        for player in players:
            player.is_minimized = player.nr >= 2

        pl = PlayerList(players)
        self.assert_is_minimized(pl, (False, False, True, True, True))
        pl.restore_and_move_up(players[-1])
        self.assert_order(pl, (0, 1, 4, 2, 3))
        self.assert_has_refreshed(pl, (False, False, True, True, True))
        self.assert_is_minimized(pl, (False, False, False, True, True))

    def test_restore_single_stays_in_place(self):
        players = [PlayerMock(nr, default_controls[nr]) for nr in range(player_count)]
        players[-1].is_minimized = True
        pl = PlayerList(players)
        self.assert_is_minimized(pl, (False, False, False, False, True))
        pl.restore_and_move_up(players[-1])
        self.assert_order(pl, (0, 1, 2, 3, 4))
        self.assert_has_refreshed(pl, (False, False, False, False, False))
        self.assert_is_minimized(pl, (False, False, False, False, False))

    def test_playerlist_is_iterable(self):
        players = [PlayerMock(nr, default_controls[nr]) for nr in range(player_count)]
        pl = PlayerList(players)

        nrs = [player.nr for player in pl]
        self.assertSequenceEqual(nrs, list(range(len(players))))

    def test_sort(self):
        players = [PlayerMock(nr, default_controls[nr]) for nr in range(player_count)]
        players[0], players[-1] = players[-1], players[0]
        players[0].control, players[-1].control = players[-1].control, players[0].control
        pl = PlayerList(players)

        pl.sort(key=lambda p:p.nr, reverse=True)
        self.assert_order(pl, (4, 3, 2, 1, 0))
        self.assert_has_refreshed(pl, (False, True, False, True, False))
