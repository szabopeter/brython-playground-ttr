import unittest

from playerlist import PlayerList


class PlayerMock:
    def __init__(self, nr, control=None):
        self.nr = nr
        self.control = PlayerControlMock(nr) if control is None else control
        self.has_refreshed = False
        self.is_minimized = False
        self.has_reset = True

    def update_all(self):
        self.has_refreshed = True

    def minimize(self):
        self.is_minimized = True

    def restore(self):
        self.is_minimized = False

    def reset(self):
        self.has_reset = True
        self.has_refreshed = True


class PlayerControlMock:
    def __init__(self, nr):
        self.nr = nr


player_count = 5
default_controls = [PlayerControlMock(nr) for nr in range(player_count)]


def create_playerlist():
    players = [PlayerMock(nr, default_controls[nr]) for nr in range(player_count)]
    pl = PlayerList(players)
    return pl, players


def clear_refresh(pl):
    for p in pl:
        p.has_refreshed = False


class PlayerListTestCase(unittest.TestCase):
    def assert_order(self, playerlist, expected_nrs):
        actual_nrs = [player.nr for player in playerlist.get_players()]
        self.assertSequenceEqual(actual_nrs, expected_nrs)

        control_nrs = [player.control.nr for player in playerlist.get_players()]
        self.assertSequenceEqual(control_nrs, list(range(len(playerlist))))

    def assert_list_property_sequence(self, playerlist, key, expected_values):
        actual_values = [key(player) for player in playerlist]
        self.assertSequenceEqual(actual_values, expected_values)

    def assert_has_refreshed(self, playerlist, expected_refresh):
        self.assert_list_property_sequence(playerlist, lambda p: p.has_refreshed, expected_refresh)

    def assert_is_minimized(self, playerlist, expected_is_minimized):
        self.assert_list_property_sequence(playerlist, lambda p: p.is_minimized, expected_is_minimized)

    def assert_has_reset(self, playerlist, expected_reset):
        self.assert_list_property_sequence(playerlist, lambda p: p.has_reset, expected_reset)

    def test_minimize_moves_to_last(self):
        pl, players = create_playerlist()
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
        pl, players = create_playerlist()
        players[-1].is_minimized = True
        self.assert_is_minimized(pl, (False, False, False, False, True))
        pl.restore_and_move_up(players[-1])
        self.assert_order(pl, (0, 1, 2, 3, 4))
        self.assert_has_refreshed(pl, (False, False, False, False, False))
        self.assert_is_minimized(pl, (False, False, False, False, False))

    def test_playerlist_is_iterable(self):
        pl, players = create_playerlist()

        nrs = [player.nr for player in pl]
        self.assertSequenceEqual(nrs, list(range(len(players))))

    def test_sort(self):
        pl, players = create_playerlist()
        players[0].nr, players[-1].nr = players[-1].nr, players[0].nr
        self.assert_order(pl, (4, 1, 2, 3, 0))

        pl.sort(key=lambda p:p.nr, reverse=True)
        self.assert_order(pl, (4, 3, 2, 1, 0))
        self.assert_has_refreshed(pl, (False, True, False, True, False))

    def test_restart(self):
        pl, players = create_playerlist()
        pl.minimize_and_move_to_last(players[1])
        clear_refresh(pl)
        pl.restart()
        self.assert_order(pl, (0, 2, 3, 4, 1))
        self.assert_has_reset(pl, (True, ) * 5)
        self.assert_is_minimized(pl, (False, False, False, False, True))

    def test_save_and_restore(self):
        pl, players = create_playerlist()
        pl.minimize_and_move_to_last(players[1])
        clear_refresh(pl)
        pl.save_order()
        pl.minimize_and_move_to_last(players[0])
        self.assert_order(pl, (2, 3, 4, 1, 0))
        self.assert_is_minimized(pl, (False, False, False, True, True))
        clear_refresh(pl)
        pl.load_order()
        self.assert_order(pl, (0, 2, 3, 4, 1))
        self.assert_has_refreshed(pl, (True, ) * 5)
        self.assert_is_minimized(pl, (False, False, False, False, True))
