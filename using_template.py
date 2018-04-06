import browser
from browser.template import Template

from playercontrol import PlayerControl
from util import show_div, hide_div


def log(msg):
    browser.doc['messages'].text = msg
    print(msg)


def log_event(msg, event, element):
    log("%r target=%r data=%r element=%r" % (msg, dir(event.target), event.target.attributes['data-divnr'].value, element, ))


from player import Player
from gameconfig import game_config

controls = [PlayerControl(i, game_config) for i in range(game_config.max_players)]

def create_players():
    return [Player(i, controls[i]) for i in range(game_config.max_players)]

players = create_players()

# TODO: these methods should be put in a class for unit-testing
def move_to_last(player_nr):
    control_nr = players[player_nr].control.nr
    for player in players:
        if player.control.nr < control_nr:
            continue
        elif player.control.nr == control_nr:
            player.control = controls[-1]
        else:
            player.control = controls[player.control.nr - 1]
        player.update_all()

def move_up(player_nr):
    control_nr = players[player_nr].control.nr
    target_control_nr = len([pl for pl in players if pl.is_minimized is False])
    for player in players:
        if player.control.nr == control_nr:
            player.control = controls[target_control_nr]
        elif target_control_nr <= player.control.nr < control_nr:
            player.control = controls[player.control.nr + 1]
        else:
            continue
        player.update_all()


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


def get_player(event):
    player_number, _ = get_divnr(event)
    for player in players:
        if player.control.nr == player_number:
            return player
    log("Could not find control for player %s" % player_number)


def increase(event, element):
    # log_event("inc", event, element)
    player_number, divnr = get_divnr(event)
    get_player(event).increase_count(divnr)


def decrease(event, element):
    # log_event("dec", event, element)
    player_number, divnr = get_divnr(event)
    get_player(event).decrease_count(divnr)


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
    # player.set_name(player.control.get_name())
    player.set_name(event.target.value)


def minimize(event, element):
    # log_event("minimize", event, element)
    player = get_player(event)
    player.minimize()
    move_to_last(player.nr)


def restore(event, element):
    # log_event("restore", event, element)
    player = get_player(event)
    move_up(player.nr)
    player.restore()


@browser.doc['set_players_go'].bind('click')
def set_players_go(event):
    dd = browser.doc['set_players']
    selected = int(dd.options[dd.selectedIndex].value)
    set_players(selected)


@browser.doc["restart"].bind('click')
def restart(event):
    show_div("confirm_restart", "inline")


@browser.doc["confirm_restart"].bind('click')
def confirm_restart(event):
    hide_div("confirm_restart")
    # TODO: suppress parent click

    global players
    names = [player.name for player in players]
    players = create_players()
    for i, player in enumerate(players):
        player.name = names[i]
        player.update_all()

# TODO event for mouse_leaving: hide confirm_restart again

def set_players(player_count):
    # log('Selected: %s' % player_count)
    events = [increase, decrease, additional_points_change,
              longest_road_length_change, minimize, restore, player_name_change]
    Template(browser.doc['players'], events).render(
        players=players, 
        train_lengths=game_config.train_lengths
        )

    for player in players:
        player.is_minimized = player.nr >= player_count
        player.update_all()

    show_div('players')
    hide_div('player_selection')


hide_div("loading")
show_div("main_menu")
# show_div('player_selection')
set_players(5)

# TODO: run browser unit tests depending on url arg
