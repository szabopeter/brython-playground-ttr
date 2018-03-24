import browser
from browser.template import Template

#browser.doc['test'].text = "hello"

length_values = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 10,
    6: 15
    }

remaining_pieces = 45
train_lengths = [1, 2, 3, 4, 5, 6]
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
    score[0] = s
    remaining[0] = r


def increase(event, element):
    # log_event("inc", event, element)
    counts[get_divnr(event)] += 1
    update_score()


def decrease(event, element):
    # log_event("dec", event, element)
    counts[get_divnr(event)] -= 1
    update_score()


Template(browser.doc['input_divs'], [increase, decrease]).render(
    train_lengths=train_lengths, count=counts, score=score, remaining=remaining)

#------------------------
lengths = {}
for i in (1, 2, 3, 4, 5, 6):
    lengths[i] = 0

def increase_click(event):
    lengths[get_divnr(event)] += 1

inc_buttons = browser.doc.select("#main_lengths DIV .increase")
for inc_button in inc_buttons:
    inc_button.addEventListener("click", increase_click)


