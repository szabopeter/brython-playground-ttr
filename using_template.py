import browser
from browser.template import Template

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
counts = {length: 0 for length in train_lengths}
score = [0]
remaining = [remaining_pieces]


def log(msg):
    browser.doc['messages'].text = msg
    print(msg)


def log_event(msg, event, element):
    log("%r target=%r data=%r element=%r" % (msg, dir(event.target), event.target.attributes['data-divnr'].value, element, ))


def get_divnr(event):
    return int(event.target.parent.attributes['data-divnr'].value)


def update_score():
    s = 0
    r = remaining_pieces
    for l in train_lengths:
        s += length_values[l] * counts[l]
        r -= l * counts[l]
    browser.doc['out_score'].text = score[0] = s
    browser.doc['out_remaining'].text = remaining[0] = r
    

def increase(event, element):
    # log_event("inc", event, element)
    divnr = get_divnr(event)
    counts[divnr] += 1
    browser.doc['count%s' % divnr].text = counts[divnr] 
    update_score()


def decrease(event, element):
    # log_event("dec", event, element)
    divnr = get_divnr(event)
    counts[divnr] -= 1
    browser.doc['count%s' % divnr].text = counts[divnr] 
    update_score()


Template(browser.doc['input_divs_wrapper'], [increase, decrease]).render(
    train_lengths=train_lengths)
Template(browser.doc['out_remaining']).render(remaining=remaining)
Template(browser.doc['out_score']).render(score=score)

