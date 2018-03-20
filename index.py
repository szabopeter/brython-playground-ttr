import browser
from browser.template import Template

#browser.doc['test'].text = "hello"

train_lengths = [1, 2, 3, 4, 5, 6]
counts = {length: 0 for length in train_lengths}

def increase(event, element):
    print("inc %s %s" % (event, element, ))
    pass

def decrease(event, element):
    print("dec %s %s" % (event, element, ))
    pass

Template(browser.doc['input_divs'], [increase, decrease]).render(train_lengths=train_lengths, count=counts)
