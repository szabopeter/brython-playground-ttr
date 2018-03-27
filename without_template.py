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


def log(msg):
    browser.doc['messages'].text = msg
    print(msg)


def log_event(msg, event, element):
    log("%r target=%r data=%r element=%r" % (msg, dir(event.target), event.target.attributes['data-divnr'].value, element, ))


lengths = {}
for i in (1, 2, 3, 4, 5, 6):
    lengths[i] = 0

inc_buttons = {}
dec_buttons = {}
length_divs = {}
length_blocks = {}


def update_out():
    s = 0
    r = 45
    # log(length_values)
    # log(lengths)
    for l in (1, 2, 3, 4, 5, 6):
        # log("tl[l] = %s, l[l] = %s" % (length_values[l], lengths[l]))
        s += length_values[l] * lengths[l]
        r -= lengths[l] * l
    # log("s=%s r=%s" % (s, r, ))
    browser.doc['score'].text = s
    browser.doc['remaining'].text = r


def mk_action(divnr):
    def inc_action(event):
        lengths[divnr] += 1
        length_divs[divnr].text = lengths[divnr]
        log("inc %s" % divnr)
        update_out()

    def dec_action(event):
        lengths[divnr] -= 1
        length_divs[divnr].text = lengths[divnr]
        log("dec %s" % divnr)
        update_out()

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


