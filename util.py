import browser


def show_div(id):
    browser.doc[id].style.display = 'block'


def hide_div(id):
    browser.doc[id].style.display = 'none'
