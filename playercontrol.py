import browser
from util import show_div, hide_div


class PlayerControl:
    def __init__(self, player_number):
        self.nr = player_number

    def update_count(self, length, count):
        if count == 0:
            count = ""
        browser.doc['count%s_%s' % (self.nr, length, )].text = count

    def update_train_score(self, train_score):
        if train_score == 0:
            train_score = ""
        browser.doc['out_score%s' % self.nr].text = train_score

    def update_total_score(self, total_score):
        browser.doc['total_score%s' % self.nr].text = total_score

    def update_remaining(self, remaining):
        div = browser.doc['out_remaining%s' % self.nr]
        if remaining is None or remaining == "":
            div.text = ""
            return

        div.text = remaining

        if remaining > 2:
            div.classList.remove('invalid')
            div.classList.remove('finished')
        elif 0 <= remaining <= 2:
            div.classList.remove('invalid')
            div.classList.add('finished')
        else:
            div.classList.remove('finished')
            div.classList.add('invalid')

    def update_additional_total(self, text):
        browser.doc['additional_total%s' % self.nr].text = text

    def get_additional_points(self):
        textbox = browser.doc['additional_points%s' % self.nr]
        return textbox.value

    def get_name(self):
        return browser.doc['player_name%s' % self.nr].value

    def update_name(self, name):
        browser.doc['player_name%s' % self.nr].value = name

    def set_tickets_entered(self, text):
        browser.doc['additional_points%s' % self.nr].value = text

    def mark_additional_points_valid(self):
        textbox = browser.doc['additional_points%s' % self.nr]
        textbox.classList.remove('invalid')
        textbox.classList.add('valid')

    def mark_additional_points_invalid(self):
        textbox = browser.doc['additional_points%s' % self.nr]
        textbox.classList.remove('valid')
        textbox.classList.add('invalid')
        self.update_additional_total("?!")

    def mark_additional_points_neutral(self):
        textbox = browser.doc['additional_points%s' % self.nr]
        textbox.classList.remove('valid')
        textbox.classList.remove('invalid')

    def set_longest_road(self, value):
        checkbox = browser.doc['longest_road%s' % self.nr]
        checkbox.checked = value

    def minimize(self):
        show_div("player_view_minimized%s" % self.nr)
        hide_div("player_view_normal%s" % self.nr)

    def restore(self):
        hide_div("player_view_minimized%s" % self.nr)
        show_div("player_view_normal%s" % self.nr)

    def update_color(self, color):
        div = browser.doc['player_section%s' % self.nr]
        class_list = div.classList
        new_color_class_name = "player_color_%s" % color
        class_list.add(new_color_class_name)
        to_remove = [class_name for class_name in class_list
                     if class_name.startswith("player_color") and class_name != new_color_class_name]

        for class_name in to_remove:
            class_list.remove(class_name)
