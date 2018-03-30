import browser
from browser.template import Template

max_players = 5
all_colors = "red green blue yellow black".split()

def show_div(id):
    browser.doc[id].style.display = 'block'

def hide_div(id):
    browser.doc[id].style.display = 'none'

show_div('player_selection')

length_values = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 10,
    6: 15,
    7: 25,
    }

remaining_pieces = 45
train_lengths = [1, 2, 3, 4, 5, 6]
counts = [{length: 0 for length in train_lengths} for p in range(max_players)]
score = [0, ] * max_players
tickets = [0, ] * max_players
total = [0, ] * max_players
remaining = [remaining_pieces, ] * max_players
colors = list(range(max_players))


def log(msg):
    browser.doc['messages'].text = msg
    print(msg)


def log_event(msg, event, element):
    log("%r target=%r data=%r element=%r" % (msg, dir(event.target), event.target.attributes['data-divnr'].value, element, ))


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


def update_total(player_number):
    total[player_number] = score[player_number] + tickets[player_number]
    log("Total for %s is %s" % (player_number, total[player_number], ))
    ctrl = browser.doc['total_score%s' % player_number]
    if ctrl:
        ctrl.text = total[player_number]


def update_score(player_number):
    s = 0
    r = remaining_pieces
    for l in train_lengths:
        s += length_values[l] * counts[player_number][l]
        r -= l * counts[player_number][l]
    browser.doc['out_score%s' % player_number].text = score[player_number] = s
    browser.doc['out_remaining%s' % player_number].text = remaining[player_number] = r
    update_total(player_number)
    

def increase(event, element):
    # log_event("inc", event, element)
    player_number, divnr = get_divnr(event)
    counts[player_number][divnr] += 1
    browser.doc['count%s_%s' % (player_number, divnr, )].text = counts[player_number][divnr] 
    update_score(player_number)


def decrease(event, element):
    # log_event("dec", event, element)
    player_number, divnr = get_divnr(event)
    counts[player_number][divnr] -= 1
    browser.doc['count%s_%s' % (player_number, divnr, )].text = counts[player_number][divnr] 
    update_score(player_number)


def additional_points_change(event, element):
    #log_event("additional pts change", event, element)
    player_number, divnr = get_divnr(event)
    textbox = browser.doc['additional_points%s' % player_number]
    log(repr(textbox.value))
    text = textbox.value
    pts = text.split()
    try:
        tickets[player_number] = points = sum([int(pt) for pt in pts])
        textbox.classList.remove('invalid')
        textbox.classList.add('valid')
        browser.doc['additional_total%s' % player_number].text = points
    except ValueError:
        textbox.classList.remove('valid')
        textbox.classList.add('invalid')
        log("Could not parse " + text)
        browser.doc['additional_total%s' % player_number].text = "?!"
        return

    update_total(player_number)

players = ["Single"]


@browser.doc['set_players_go'].bind('click')
def set_players_go(event):
    dd = browser.doc['set_players']
    selected = int(dd.options[dd.selectedIndex].value)
    set_players(selected)


def set_players(player_count):
    log('Selected: %s' % player_count)
    players = ["Mr. " + all_colors[i].capitalize() for i in range(player_count)]
    events = [increase, decrease, additional_points_change]
    Template(browser.doc['players'], events).render(
        players=players, 
        train_lengths=train_lengths,
        all_colors=all_colors,
        colors=colors
        )

    show_div('players')
    hide_div('player_selection')

hide_div('loading')
# show_div('player_selection')
set_players(5)

