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

def get_count_ctr(nr):
    browser.doc['']

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

# ------------------------

lengths = {}
for i in (1, 2, 3, 4, 5, 6):
    lengths[i] = 0

inc_buttons = {}
dec_buttons = {}
length_divs = {}
length_blocks = {}

def mk_action(divnr):
    def inc_action(event):
        lengths[divnr] += 1
        length_divs[divnr].text = lengths[divnr]
        log("inc %s" % divnr)

    def dec_action(event):
        lengths[divnr] -= 1
        length_divs[divnr].text = lengths[divnr]
        log("dec %s" % divnr)
    
    return inc_action, dec_action
    

for length_block in browser.doc.select("#main_lengths DIV.length_block"):
    # if 'datadivnr' not in length_block.attributes:
    #    log("skip %s, has no datadivnr" % length_block)
    #    continue
    divnr_str = length_block.attributes['datadivnr']
    if not divnr_str:
        log("skipping %s, has no datadivnr" % length_block)
        continue
    divnr = int(divnr_str.value)

    length_blocks[divnr] = length_block
    inc_button = length_block.select('.increase')[0]
    dec_button = length_block.select('.decrease')[0]
    inc_buttons[divnr] = inc_button
    dec_buttons[divnr] = dec_button
    length_divs[divnr] = length_block.select('.value')[0]

    def inc_action1(event):
        lengths[divnr] += 1
        length_block.text = lengths[divnr]
        log("inc %s" % divnr)

    def dec_action1(event):
        lengths[divnr] -= 1
        length_block.text = lengths[divnr]
        log("dec %s" % divnr)

    inc_action, dec_action = mk_action(divnr)
    inc_button.bind("click", inc_action)
    dec_button.bind("click", dec_action)


