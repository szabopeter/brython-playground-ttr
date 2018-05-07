import browser


class BrythonFunctions:
    def get_element(self, entity_id):
        return browser.doc[entity_id]

    def show(self, id, value="block"):
        self.get_element(id).style.display = value

    def hide(self, id):
        self.get_element(id).style.display = "none"

    # TODO: reuse these in PlayerControl
    def add_class(self, entity_id, css_class):
        self.get_element(entity_id).classList.add(css_class)

    def remove_class(self, entity_id, css_class):
        self.get_element(entity_id).classList.remove(css_class)
