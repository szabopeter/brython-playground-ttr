from brythonfunctions import BrythonFunctions


# TODO: consider in-browser integration tests to ensure valid ids here
class PlayerControl:
    def __init__(self, player_number, game_config, brython_functions=None):
        self.nr = player_number
        self.all_player_colors = [self.player_color(color) for color in game_config.all_colors]
        self.game_config = game_config
        self.brython = brython_functions if brython_functions is not None else BrythonFunctions()

    def get_element(self, prefix, args=None):
        if args is None:
            args = (self.nr, )
        eid = prefix + "_".join([str(arg) for arg in args])
        return self.brython.get_element(eid)

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
        self.mark_remaining(remaining)

    def mark_remaining(self, remaining):
        if remaining > self.game_config.max_pieces_for_finishing:
            self.mark_with_class("out_remaining", None, "invalid", "finished")
        elif 0 <= remaining:
            self.mark_with_class("out_remaining", "finished", "invalid")
        else:
            self.mark_with_class("out_remaining", "invalid", "finished")

    def update_additional_total(self, text):
        self.get_element("additional_total").text = text

    def update_name(self, name):
        self.get_element("player_name").value = name

    def set_tickets_entered(self, text):
        self.get_element("additional_points").value = text

    # noinspection PyMethodMayBeStatic
    def mark_control_with_class(self, class_list, to_add, to_remove):
        if to_add is not None:
            class_list.add(to_add)

        for class_name in to_remove:
            if class_name != to_add:
                class_list.remove(class_name)

    def mark_with_class(self, prefix, to_add, *to_remove):
        # print("Marking %s with %s instead of %s" % (prefix, to_add, to_remove))
        control = self.get_element(prefix)
        self.mark_control_with_class(control.classList, to_add, to_remove)

    def mark_additional_points_valid(self):
        self.mark_with_class("additional_points", "valid", "invalid")

    def mark_additional_points_invalid(self):
        self.mark_with_class("additional_points", "invalid", "valid")
        self.update_additional_total("?!")

    def mark_additional_points_neutral(self):
        self.mark_with_class("additional_points", None, "invalid", "valid")

    def set_has_longest_road(self, value):
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
        self.mark_with_class("longest_road_length", "invalid", "valid")

    def mark_longest_road_length_valid(self):
        self.mark_with_class("longest_road_length", "valid", "invalid")

    def mark_longest_road_length_neutral(self):
        self.mark_with_class("longest_road_length", None, "valid", "invalid")

    def minimize(self):
        self.brython.show("player_view_minimized%s" % self.nr)
        self.brython.hide("player_view_normal%s" % self.nr)

    def restore(self):
        self.brython.hide("player_view_minimized%s" % self.nr)
        self.brython.show("player_view_normal%s" % self.nr)

    # noinspection PyMethodMayBeStatic
    def player_color(self, color):
        return "player_color_%s" % color

    def update_color(self, color):
        new_color_class_name = self.player_color(color)
        self.mark_with_class("player_section", new_color_class_name, *self.all_player_colors)
