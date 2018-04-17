import browser
from browser.template import Template

from brythonfunctions import BrythonFunctions

from playercontrol import PlayerControl
from playerlist import PlayerList
from player import Player
from gameconfig import game_config


def log(msg):
    browser.doc['messages'].text = msg
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


# TODO: move logic to playerlist
def longest_road_length_change(event, element):
    # log_event("lrl_change", event, element)
    player = get_player(event)
    player.set_longest_road_length_entered(event.target.value)
    lengths = [player.longest_road_length for player in players if player.longest_road_length]
    if lengths:
        longest = max(lengths)
        for player in players:
            if player.longest_road_length is not None:
                has_longest = player.longest_road_length == longest
                player.set_longest_road(has_longest)


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


# TODO move logic to playerlist
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


brython_functions.hide("loading")
brython_functions.show("main_menu")
# brython_functions.show('player_selection')
set_players(5)
# brython_functions.hide('player_selection')

# TODO: run browser unit tests depending on url arg

