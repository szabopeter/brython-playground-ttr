import browser


class BrythonFunctions:
    def get_element(self, entity_id):
        return browser.doc[entity_id]

    def show(self, id):
        browser.doc[id].style.display = 'block'

    def hide(self, id):
        browser.doc[id].style.display = 'none'