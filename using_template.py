import browser
from browser.template import Template


def log(msg):
    browser.doc['messages'].text = msg
    print(msg)


def log_event(msg, event, element):
    log("%r target=%r data=%r element=%r" % (msg, dir(event.target), event.target.attributes['data-divnr'].value, element, ))


def show_div(id):
    browser.doc[id].style.display = 'block'


def hide_div(id):
    browser.doc[id].style.display = 'none'


class PlayerControl:
    def __init__(self, player_number):
        self.nr = player_number

    def update_count(self, length, count):
        browser.doc['count%s_%s' % (self.nr, length, )].text = count

    def update_train_score(self, train_score):
        browser.doc['out_score%s' % self.nr].text = train_score

    def update_total_score(self, total_score):
        browser.doc['total_score%s' % self.nr].text = total_score

    def update_remaining(self, remaining):
        div = browser.doc['out_remaining%s' % self.nr]
        div.text = remaining
        if remaining > 2:
            div.classList.remove('invalid')
            div.classList.remove('finished')
        elif 0 <= remaining <= 2:
            div.classList.remove('invalid')
            div.classList.add('finished')
        else:
            div.classList.remove('finished')
            div.classList.add('invalid')

    def update_additional_total(self, text):
        browser.doc['additional_total%s' % self.nr].text = text

    def get_additional_points(self):
        textbox = browser.doc['additional_points%s' % self.nr]
        return textbox.value

    def get_name(self):
        return browser.doc['player_name%s' % self.nr].value

    def update_name(self, name):
        browser.doc['player_name%s' % self.nr].value = name

    def set_tickets_entered(self, text):
        browser.doc['additional_points%s' % self.nr].value = text

    def mark_additional_points_valid(self):
        textbox = browser.doc['additional_points%s' % self.nr]
        textbox.classList.remove('invalid')
        textbox.classList.add('valid')

    def mark_additional_points_invalid(self):
        textbox = browser.doc['additional_points%s' % self.nr]
        textbox.classList.remove('valid')
        textbox.classList.add('invalid')
        self.update_additional_total("?!")

    def set_longest_road(self, value):
        checkbox = browser.doc['longest_road%s' % self.nr]
        checkbox.checked = value

    def minimize(self):
        show_div("player_view_minimized%s" % self.nr)
        hide_div("player_view_normal%s" % self.nr)

    def restore(self):
        hide_div("player_view_minimized%s" % self.nr)
        show_div("player_view_normal%s" % self.nr)

    def update_color(self, color):
        div = browser.doc['player_section%s' % self.nr]
        class_list = div.classList
        new_color_class_name = "player_color_%s" % color
        class_list.add(new_color_class_name)
        to_remove = [class_name for class_name in class_list
                     if class_name.startswith("player_color") and class_name != new_color_class_name]

        for class_name in to_remove:
            class_list.remove(class_name)


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


def check_longest_road(event, element):
    # log_event("longest", event, element)
    player_number = get_player(event).nr
    for player in players:
        has_longest_road = player.nr == player_number and event.target.checked
        player.set_longest_road(has_longest_road)


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
              check_longest_road, minimize, restore, player_name_change]
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

