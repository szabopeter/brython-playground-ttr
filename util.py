import browser


def show_div(id, value="block"):
    browser.doc[id].style.display = value


def hide_div(id):
    browser.doc[id].style.display = "none"
