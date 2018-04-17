import unittest

from playerlist import PlayerList


class PlayerMock:
    def __init__(self, nr, control=None):
        self.nr = nr
        self.control = PlayerControlMock(nr) if control is None else control
        self.has_refreshed = False
        self.is_minimized = False
        self.has_reset = True
        self.total_score = 0

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
        pl.can_save = False
        pl.minimize_and_move_to_last(players[0])
        self.assert_order(pl, (2, 3, 4, 1, 0))
        self.assert_is_minimized(pl, (False, False, False, True, True))
        clear_refresh(pl)
        pl.load_order()
        self.assert_order(pl, (0, 2, 3, 4, 1))
        self.assert_has_refreshed(pl, (True, ) * 5)
        self.assert_is_minimized(pl, (False, False, False, False, True))

    def test_get_by_control_nr(self):
        pl, players = create_playerlist()
        pl.minimize_and_move_to_last(players[1])
        self.assertEqual(players[0], pl[0])
        self.assertEqual(players[1], pl[4])
        self.assertEqual(players[2], pl[1])
        self.assertEqual(players[3], pl[2])
        self.assertEqual(players[4], pl[3])

    def test_restart_reloading(self):
        pl, (red, green, blue, yellow, black) = create_playerlist()
        for p in (green, blue, black):
            pl.minimize_and_move_to_last(p)
        pl.restore_and_move_up(blue)
        self.assert_order(pl, (red.nr, yellow.nr, blue.nr, green.nr, black.nr))
        self.assert_is_minimized(pl, (False, False, False, True, True))
        # Red, Yellow and Blue set up a game

        red.total_score = 5
        yellow.total_score = 11
        blue.total_score = 22
        black.total_score = -1
        # They played some, scored some and decided to finish the game

        pl.finish()
        self.assertFalse(pl.can_save)
        self.assert_order(pl, (blue.nr, yellow.nr, red.nr, green.nr, black.nr))

        pl.minimize_and_move_to_last(red)
        self.assertFalse(pl.can_save)
        self.assert_order(pl, (blue.nr, yellow.nr, green.nr, black.nr, red.nr))
        # Blue and Yellow decided to continue just for fun, Yellow does not

        blue.total_score = 22
        yellow.total_score = 33
        pl.finish()
        self.assertFalse(pl.can_save)
        self.assert_order(pl, (yellow.nr, blue.nr, red.nr, green.nr, black.nr))
        # So the two played a bit, changed the ranking and finished the extended game

        pl.restart()
        self.assertTrue(pl.can_save)
        self.assert_order(pl, (red.nr, yellow.nr, blue.nr, green.nr, black.nr))
        self.assert_is_minimized(pl, (False, False, False, True, True))
        # The trio wants to play again and restart the game
