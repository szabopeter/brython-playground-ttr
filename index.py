import browser
from browser.template import Template

from brythonfunctions import BrythonFunctions

from playercontrol import PlayerControl
from playerlist import PlayerList
from player import Player
from gameconfig import game_config


def log(msg):
    browser.doc['messages_content'].text = msg
    print(msg)


def log_event(msg, event, element):
    log("%r target=%r data=%r element=%r" % (msg, dir(event.target), event.target.attributes['data-divnr'].value, element, ))


brython_functions = BrythonFunctions()

def create_players(player_count):
    return [Player(i, PlayerControl(i, game_config)) for i in range(player_count)]

players = PlayerList(create_players(game_config.max_players))


def get_divnr(event):
    attrib = event.target.attributes['data-divnr']

    if not attrib:
        attrib = event.target.parent.attributes['data-divnr']

    if not attrib:
        log("Could not find data-divnr attribute!")
        log_event("get_divnr", event, None)
        return 0, 0

    data_divnr = attrib.value
    player_number, divnr = [int(x) for x in data_divnr.split('_')]
    return player_number, divnr


def get_player(event_or_nr):
    if isinstance(event_or_nr, int):
        player_number = event_or_nr
    else:
        player_number, _ = get_divnr(event_or_nr)
    return players[player_number]


def increase(event, element):
    # log_event("inc", event, element)
    player_number, divnr = get_divnr(event)
    get_player(player_number).increase_count(divnr)


def decrease(event, element):
    # log_event("dec", event, element)
    player_number, divnr = get_divnr(event)
    get_player(player_number).decrease_count(divnr)


def longest_road_length_change(event, element):
    # log_event("lrl_change", event, element)
    player = get_player(event)
    player.set_longest_road_length_entered(event.target.value)
    players.recalculate_longest_roads()


def additional_points_change(event, element):
    # log_event("additional pts change", event, element)
    player = get_player(event)
    error = player.set_tickets_entered(event.target.value)
    if error is not None:
        log(error)


def player_name_change(event, element):
    player = get_player(event)
    player.set_name(event.target.value)


def minimize(event, element):
    # log_event("minimize", event, element)
    player = get_player(event)
    players.minimize_and_move_to_last(player)


def restore(event, element):
    # log_event("restore", event, element)
    player = get_player(event)
    players.restore_and_move_up(player)


@browser.doc['set_players_go'].bind('click')
def set_players_go(event):
    dd = browser.doc['set_players']
    selected = int(dd.options[dd.selectedIndex].value)
    set_players(selected)


@browser.doc["restart"].bind('click')
def restart(event):
    brython_functions.show("confirm_restart", "inline")


@browser.doc["restart"].bind('mouseleave')
def restart_leave(event):
    brython_functions.hide("confirm_restart")


@browser.doc["confirm_restart"].bind('click')
def confirm_restart(event):
    brython_functions.hide("confirm_restart")
    event.stopPropagation()
    players.restart()


@browser.doc["finish"].bind('click')
def finish(event):
    brython_functions.show("confirm_finish", "inline")


@browser.doc["finish"].bind('mouseleave')
def finish_leave(event):
    brython_functions.hide("confirm_finish")


@browser.doc["confirm_finish"].bind('click')
def confirm_finish(event):
    brython_functions.hide("confirm_finish")
    event.stopPropagation()
    players.finish()


@browser.doc["save_to_browser"].bind('click')
def save_to_browser(event):
    brython_functions.show("confirm_save_to_browser", "inline")


@browser.doc["save_to_browser"].bind('mouseleave')
def save_to_browser_leave(event):
    brython_functions.hide("confirm_save_to_browser")


@browser.doc["confirm_save_to_browser"].bind('click')
def confirm_save_to_browser(event):
    brython_functions.hide("confirm_save_to_browser")
    event.stopPropagation()
    save_to_local_storage()


@browser.doc["load_from_browser"].bind('click')
def load_from_browser(event):
    brython_functions.show("confirm_load_from_browser", "inline")


@browser.doc["load_from_browser"].bind('mouseleave')
def load_from_browser_leave(event):
    brython_functions.hide("confirm_load_from_browser")


@browser.doc["confirm_load_from_browser"].bind('click')
def confirm_load_from_browser(event):
    brython_functions.hide("confirm_load_from_browser")
    event.stopPropagation()
    load_from_local_storage()


def load_from_local_storage():
    log("Loading...")

    from browser.local_storage import storage
    import json

    json_dump = storage['playerlist']
    log("Json:")
    log(json_dump)

    ser = json.loads(json_dump)
    log("Serializeable")
    log(str(ser))

    global players

    def player_from_serializeable(serializeable, control_nr):
        control = PlayerControl(control_nr, game_config)
        return Player.from_serializeable(serializeable, control)
    players = PlayerList.from_serializeable(ser, player_from_serializeable)

    players.update_all()


def save_to_local_storage():
    log("Saving...")
    from browser.local_storage import storage
    import json
    ser = players.serializeable()
    log("Serializeable:")
    log(str(ser))
    json_dump = json.dumps(ser)
    log("Json:")
    log(json_dump)
    storage['playerlist'] = json_dump
    log("Saved...")
    # TODO: show checkmark on UI
    # local storage example
    # from browser.local_storage import storage
    # try:
    #     storage['tasklist']
    # except:
    #     storage['tasklist'] = json.dumps({})
    #
    # self.tasks = json.loads(storage['tasklist'])
    # storage['tasklist'] = json.dumps(self.tasks)


def set_players(player_count):
    # log('Selected: %s' % player_count)
    global players
    players = PlayerList(create_players(player_count))
    events = [increase, decrease, additional_points_change,
              longest_road_length_change, minimize, restore, player_name_change]
    Template(browser.doc['players'], events).render(
        players=players, 
        train_lengths=game_config.train_lengths
        )

    valid, message = players.is_valid()
    if not valid:
        log(message)
        return

    for player in players:
        player.update_all()

    brython_functions.show('players')


url = browser.doc.location.toString()
unittesting = "mode=run_unittests" in url

if not unittesting:
    brython_functions.hide("loading")
    brython_functions.show("main_menu")
    # brython_functions.show('player_selection')
    set_players(5)
    # brython_functions.hide('player_selection')

else:
    brython_functions.hide("loading")
    brython_functions.show("testreport")

    def set_report_text(text):
        browser.doc["testreport"].text = text

    import unittest
    import io
    import sys

    import test_player
    import test_controlid
    import test_playerlist
    import test_storage

    testcases = [
        test_player.PlayerTestCase,
        test_controlid.ControlIdTestCase,
        test_playerlist.PlayerListTestCase,
        test_storage.JsonTestCase,
    ]

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for testcase in testcases:
        suite.addTests(loader.loadTestsFromTestCase(testcase))

    set_report_text("Executing {count} test case(s), please wait...".format(count=suite.countTestCases()))

    report_stream = io.StringIO()
    unittest.TextTestRunner(verbosity=2, stream=report_stream).run(suite)
    report = report_stream.getvalue()

    sys.stderr.write(report)
    set_report_text(report)
