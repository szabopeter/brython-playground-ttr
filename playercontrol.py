from controlid import ControlIdFactory


def get_real_brython_functions():
    from brythonfunctions import BrythonFunctions
    return BrythonFunctions()


class PlayerControl:
    def __init__(self, player_number, game_config, brython_functions=None):
        self.nr = player_number
        self.all_player_colors = [self.player_color(color) for color in game_config.all_colors]
        self.game_config = game_config
        self.brython = brython_functions if brython_functions is not None else get_real_brython_functions()

        cif = self.cid_factory = ControlIdFactory(self.brython, self.nr)
        self.CID_COUNT = {tl: cif.create("count", tl) for tl in game_config.train_lengths}
        self.CID_OUT_SCORE = cif.create("out_score")
        self.CID_TOTAL_SCORE = cif.create("total_score")
        self.CID_OUT_REMAINING = cif.create("out_remaining")
        self.CID_ADDITIONAL_TOTAL = cif.create("additional_total")
        self.CID_PLAYER_NAME = cif.create("player_name")
        self.CID_ADDITIONAL_POINTS = cif.create("additional_points")
        self.CID_LONGEST_ROAD_LENGTH = cif.create("longest_road_length")
        self.CID_PLAYER_VIEW_MINIMIZED = cif.create("player_view_minimized")
        self.CID_PLAYER_VIEW_NORMAL = cif.create("player_view_normal")
        self.CID_PLAYER_SECTION = cif.create("player_section")

    def get_all_control_ids(self):
        return self.cid_factory.created

    def is_valid(self):
        return self.cid_factory.is_valid()

    def update_count(self, length, count):
        if count == 0:
            count = ""

        self.CID_COUNT[length].get().text = count

    def update_train_score(self, train_score):
        if train_score == 0:
            train_score = ""

        self.CID_OUT_SCORE.get().text = train_score

    def update_total_score(self, total_score):
        self.CID_TOTAL_SCORE.get().text = total_score

    def update_remaining(self, remaining):
        div = self.CID_OUT_REMAINING.get()
        if remaining is None or remaining == "":
            div.text = ""
            return

        div.text = remaining
        self.mark_remaining(remaining)

    def mark_remaining(self, remaining):
        if remaining > self.game_config.max_pieces_for_finishing:
            self.mark_with_class(self.CID_OUT_REMAINING, None, "invalid", "finished")
        elif 0 <= remaining:
            self.mark_with_class(self.CID_OUT_REMAINING, "finished", "invalid")
        else:
            self.mark_with_class(self.CID_OUT_REMAINING, "invalid", "finished")

    def update_additional_total(self, text):
        self.CID_ADDITIONAL_TOTAL.get().text = text

    def update_name(self, name):
        self.CID_PLAYER_NAME.get().value = name

    def set_tickets_entered(self, text):
        self.CID_ADDITIONAL_POINTS.get().value = text

    # noinspection PyMethodMayBeStatic
    def mark_control_with_class(self, class_list, to_add, to_remove):
        if to_add is not None:
            class_list.add(to_add)

        for class_name in to_remove:
            if class_name != to_add:
                class_list.remove(class_name)

    def mark_with_class(self, controlId, to_add, *to_remove):
        # print("Marking %s with %s instead of %s" % (prefix, to_add, to_remove))
        self.mark_control_with_class(controlId.get().classList, to_add, to_remove)

    def mark_additional_points_valid(self):
        self.mark_with_class(self.CID_ADDITIONAL_POINTS, "valid", "invalid")

    def mark_additional_points_invalid(self):
        self.mark_with_class(self.CID_ADDITIONAL_POINTS, "invalid", "valid")
        self.update_additional_total("?!")

    def mark_additional_points_neutral(self):
        self.mark_with_class(self.CID_ADDITIONAL_POINTS, None, "invalid", "valid")

    def set_has_longest_road(self, value):
        classlist = self.CID_LONGEST_ROAD_LENGTH.get().classList
        if value:
            classlist.add('has_longest_road')
        else:
            classlist.remove('has_longest_road')

    def set_longest_road_length(self, value):
        if value == 0:
            value = ""

        self.CID_LONGEST_ROAD_LENGTH.get().value = value

    def mark_longest_road_length_invalid(self):
        self.mark_with_class(self.CID_LONGEST_ROAD_LENGTH, "invalid", "valid")

    def mark_longest_road_length_valid(self):
        self.mark_with_class(self.CID_LONGEST_ROAD_LENGTH, "valid", "invalid")

    def mark_longest_road_length_neutral(self):
        self.mark_with_class(self.CID_LONGEST_ROAD_LENGTH, None, "valid", "invalid")

    def minimize(self):
        self.brython.show(self.CID_PLAYER_VIEW_MINIMIZED.cid)
        self.brython.hide(self.CID_PLAYER_VIEW_NORMAL.cid)

    def restore(self):
        self.brython.hide(self.CID_PLAYER_VIEW_MINIMIZED.cid)
        self.brython.show(self.CID_PLAYER_VIEW_NORMAL.cid)

    # noinspection PyMethodMayBeStatic
    def player_color(self, color):
        return "player_color_%s" % color

    def update_color(self, color):
        new_color_class_name = self.player_color(color)
        self.mark_with_class(self.CID_PLAYER_SECTION, new_color_class_name, *self.all_player_colors)
