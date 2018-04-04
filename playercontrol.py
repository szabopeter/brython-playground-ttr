import browser
from util import show_div, hide_div


class PlayerControl:
    def __init__(self, player_number):
        self.nr = player_number

    def get_element(self, prefix, args=None):
        if args is None:
            args = (self.nr, )
        eid = prefix + "_".join([str(arg) for arg in args])
        return browser.doc[eid]

    def update_count(self, length, count):
        if count == 0:
            count = ""

        self.get_element("count", (self.nr, length)).text = count

    def update_train_score(self, train_score):
        if train_score == 0:
            train_score = ""

        self.get_element("out_score").text = train_score

    def update_total_score(self, total_score):
        self.get_element("total_score").text = total_score

    def update_remaining(self, remaining):
        div = self.get_element("out_remaining")
        if remaining is None or remaining == "":
            div.text = ""
            return

        div.text = remaining

        # TODO: these constants belong to GameConfig, the logic to Player
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
        self.get_element("additional_total").text = text

    def update_name(self, name):
        self.get_element("player_name").value = name

    def set_tickets_entered(self, text):
        self.get_element("additional_points").value = text

    def mark_additional_points_valid(self):
        textbox = self.get_element("additional_points")
        textbox.classList.remove('invalid')
        textbox.classList.add('valid')

    def mark_additional_points_invalid(self):
        textbox = self.get_element("additional_points")
        textbox.classList.remove('valid')
        textbox.classList.add('invalid')
        self.update_additional_total("?!")

    def mark_additional_points_neutral(self):
        textbox = self.get_element("additional_points")
        textbox.classList.remove('valid')
        textbox.classList.remove('invalid')

    def set_longest_road(self, value):
        classlist = self.get_element("longest_road_length").classList
        if value:
            classlist.add('has_longest_road')
        else:
            classlist.remove('has_longest_road')

    def set_longest_road_length(self, value):
        if value == 0:
            value = ""

        self.get_element("longest_road_length").value = value

    def mark_longest_road_length_invalid(self):
        textbox = self.get_element("longest_road_length")
        classlist = textbox.classList
        classlist.add('invalid')
        classlist.remove('valid')

    def mark_longest_road_length_valid(self):
        textbox = self.get_element("longest_road_length")
        classlist = textbox.classList
        classlist.add('valid')
        classlist.remove('invalid')

    def mark_longest_road_length_neutral(self):
        textbox = self.get_element("longest_road_length")
        classlist = textbox.classList
        classlist.remove('valid')
        classlist.remove('invalid')

    def minimize(self):
        show_div("player_view_minimized%s" % self.nr)
        hide_div("player_view_normal%s" % self.nr)

    def restore(self):
        hide_div("player_view_minimized%s" % self.nr)
        show_div("player_view_normal%s" % self.nr)

    def update_color(self, color):
        div = self.get_element("player_section")
        class_list = div.classList
        new_color_class_name = "player_color_%s" % color
        class_list.add(new_color_class_name)
        to_remove = [class_name for class_name in class_list
                     if class_name.startswith("player_color") and class_name != new_color_class_name]

        for class_name in to_remove:
            class_list.remove(class_name)
