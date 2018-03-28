import browser
from browser.template import Template

max_players = 5


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
train_lengths = [1, 2, 3, 4, 5, 6, 7]
counts = [{length: 0 for length in train_lengths} for p in range(max_players)]
score = [0,] * max_players
remaining = [remaining_pieces, ] * max_players


def log(msg):
    browser.doc['messages'].text = msg
    print(msg)


def log_event(msg, event, element):
    log("%r target=%r data=%r element=%r" % (msg, dir(event.target), event.target.attributes['data-divnr'].value, element, ))


def get_divnr(event):
    data_divnr = event.target.parent.attributes['data-divnr'].value
    player_number, divnr = [int(x) for x in data_divnr.split('_')]
    return player_number, divnr


def update_score(player_number):
    s = 0
    r = remaining_pieces
    for l in train_lengths:
        s += length_values[l] * counts[player_number][l]
        r -= l * counts[player_number][l]
    browser.doc['out_score%s' % player_number].text = score[player_number] = s
    browser.doc['out_remaining%s' % player_number].text = remaining[player_number] = r
    

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

players = ["Single"]

@browser.doc['set_players_go'].bind('click')
def set_players(event):
    dd = browser.doc['set_players']
    selected = int(dd.options[dd.selectedIndex].value)
    log('Selected: %s' % selected)
    players = ["pl#%s" % i for i in range(selected)]
    Template(browser.doc['players'], [increase, decrease]).render(players=players, train_lengths=train_lengths)
    #for i in range(selected):
    #    div_id = "input_divs_wrapper%s" % i
    #    Template(browser.doc[div_id], [increase, decrease]).render(train_lengths=train_lengths)

    show_div('players')
    hide_div('player_selection')

# Template(browser.doc['out_remaining']).render(remaining=remaining)
# Template(browser.doc['out_score']).render(score=score)
hide_div('loading')
show_div('player_selection')


