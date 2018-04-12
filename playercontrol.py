from brythonfunctions import BrythonFunctions


class ControlId:
    def __init__(self, prefix, *args):
        self.cid = prefix + "_".join([str(arg) for arg in args])


# TODO: consider in-browser integration tests to ensure valid ids here
class PlayerControl:
    def __init__(self, player_number, game_config, brython_functions=None):
        self.nr = player_number
        self.all_player_colors = [self.player_color(color) for color in game_config.all_colors]
        self.game_config = game_config
        self.brython = brython_functions if brython_functions is not None else BrythonFunctions()

        nr = player_number
        self.CID_COUNT = {tl: ControlId("count", nr, tl) for tl in game_config.train_lengths}
        self.CID_OUT_SCORE = ControlId("out_score", nr)
        self.CID_TOTAL_SCORE = ControlId("total_score", nr)
        self.CID_OUT_REMAINING = ControlId("out_remaining", nr)
        self.CID_ADDITIONAL_TOTAL = ControlId("additional_total", nr)
        self.CID_PLAYER_NAME = ControlId("player_name", nr)
        self.CID_ADDITIONAL_POINTS = ControlId("additional_points", nr)
        self.CID_LONGEST_ROAD_LENGTH = ControlId("longest_road_length", nr)
        self.CID_PLAYER_VIEW_MINIMIZED = ControlId("player_view_minimized", nr)
        self.CID_PLAYER_VIEW_NORMAL = ControlId("player_view_normal", nr)
        self.CID_PLAYER_SECTION = ControlId("player_section", nr)

    def is_valid(self):
        def get_cid(name):
            member = getattr(self, name)
            if isinstance(member, ControlId):
                return member
            return None

        missing = []
        cids = [get_cid(name) for name in dir(self)]
        for cid in cids:
            if cid is None:
                continue

            try:
                self.get_element(cid)
            except KeyError:
                missing.append(cid.cid)

        if len(missing) == 0:
            return True, None
        message = "Can't find required ids: {idlist}".format(idlist=", ".join(missing))
        return False, message

    def get_element(self, prefix, args=None):
        if isinstance(prefix, ControlId):
            eid = prefix.cid
        else:
            if args is None:
                args = (self.nr, )
            eid = prefix + "_".join([str(arg) for arg in args])
        return self.brython.get_element(eid)

    def update_count(self, length, count):
        if count == 0:
            count = ""

        self.get_element(self.CID_COUNT[length], (self.nr, length)).text = count

    def update_train_score(self, train_score):
        if train_score == 0:
            train_score = ""

        self.get_element(self.CID_OUT_SCORE).text = train_score

    def update_total_score(self, total_score):
        self.get_element(self.CID_TOTAL_SCORE).text = total_score

    def update_remaining(self, remaining):
        div = self.get_element(self.CID_OUT_REMAINING)
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
        self.get_element(self.CID_ADDITIONAL_TOTAL).text = text

    def update_name(self, name):
        self.get_element(self.CID_PLAYER_NAME).value = name

    def set_tickets_entered(self, text):
        self.get_element(self.CID_ADDITIONAL_POINTS).value = text

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
        self.mark_with_class(self.CID_ADDITIONAL_POINTS, "valid", "invalid")

    def mark_additional_points_invalid(self):
        self.mark_with_class(self.CID_ADDITIONAL_POINTS, "invalid", "valid")
        self.update_additional_total("?!")

    def mark_additional_points_neutral(self):
        self.mark_with_class(self.CID_ADDITIONAL_POINTS, None, "invalid", "valid")

    def set_has_longest_road(self, value):
        classlist = self.get_element(self.CID_LONGEST_ROAD_LENGTH).classList
        if value:
            classlist.add('has_longest_road')
        else:
            classlist.remove('has_longest_road')

    def set_longest_road_length(self, value):
        if value == 0:
            value = ""

        self.get_element(self.CID_LONGEST_ROAD_LENGTH).value = value

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
