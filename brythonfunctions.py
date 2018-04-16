import browser


class BrythonFunctions:
    def get_element(self, entity_id):
        return browser.doc[entity_id]

    def show(self, id, value="block"):
        self.get_element(id).style.display = value

    def hide(self, id):
        self.get_element(id).style.display = "none"

