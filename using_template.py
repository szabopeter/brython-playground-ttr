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

players = [Player(i, PlayerControl(i)) for i in range(game_config.max_players)]


def get_divnr(event):
    attrib = event.target.attributes['data-divnr']

    if not attrib:
        attrib = event.target.parent.attributes['data-divnr']

    if not attrib:
        log("Could not find data-divnr attribute!")
        log_event(event)
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
    get_player(event).control.minimize()

def restore(event, element):
    # log_event("restore", event, element)
    get_player(event).control.restore()


@browser.doc['set_players_go'].bind('click')
def set_players_go(event):
    dd = browser.doc['set_players']
    selected = int(dd.options[dd.selectedIndex].value)
    set_players(selected)


def set_players(player_count):
    log('Selected: %s' % player_count)
    events = [increase, decrease, additional_points_change,
              longest_road_length_change, minimize, restore, player_name_change]
    Template(browser.doc['players'], events).render(
        players=players, 
        train_lengths=game_config.train_lengths
        )

    for player in players:
        player.control.restore()

    show_div('players')
    hide_div('player_selection')


hide_div('loading')
# show_div('player_selection')
set_players(5)

# players[0].control, players[1].control = players[1].control, players[0].control
# players[0].update_all()
# players[1].update_all()
