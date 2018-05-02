from gameconfig import game_config


# TODO: consider separating control-related data (*entered) from "actual" data

class Player:
    def __init__(self, player_number, player_control):
        self.nr = player_number
        self.counts = {length: 0 for length in game_config.train_lengths}
        self.train_score = 0
        self.ticket_score = 0
        self.total_score = 0
        self.remaining = game_config.remaining_pieces
        self.color_nr = player_number
        self.control = player_control
        self.name = "Mr. " + self.color().capitalize()
        self.longest_road = False
        self.tickets_entered = ""
        self.longest_road_length_entered = ""
        self.longest_road_length = 0
        self.is_minimized = False

    def __eq__(self, other):
        return self.nr == other.nr

    def serializeable(self):
        class FieldData:
            def __init__(self, obj, name):
                self.name = name
                self.value = getattr(obj, name)
                self.type_name = self.value.__class__

        serializeable_types = (bool, int, str, list, tuple, dict)
        fields = [FieldData(self, attr_name) for attr_name in dir(self)]
        fields = [f for f in fields
                  if f.type_name in serializeable_types
                  and not f.name.startswith("__")]
        field_dict = {f.name: f.value for f in fields}
        return field_dict

    @staticmethod
    def from_serializeable(serializeable, control=None):
        nr = serializeable['nr']
        player = Player(nr, control)
        for name, value in serializeable.items():
            # print("Setting {name}={value} on {player}".format(name=name, value=value, player=player))
            setattr(player, name, value)

        player.counts = {int(key): int(value) for key, value in player.counts.items()}
        return player

    def reset(self):
        self.counts = {length: 0 for length in game_config.train_lengths}
        self.train_score = 0
        self.ticket_score = 0
        self.total_score = 0
        self.remaining = game_config.remaining_pieces
        self.longest_road = False
        self.tickets_entered = ""
        self.longest_road_length_entered = ""
        self.longest_road_length = 0
        self.update_all()

    def color(self):
        return game_config.all_colors[self.color_nr]

    def set_color_nr(self, new_color_nr):
        self.color_nr = new_color_nr
        self.control.update_color(self.color())

    def increase_count(self, length):
        self.update_count(length, self.counts[length] + 1)

    def decrease_count(self, length):
        self.update_count(length, self.counts[length] - 1)

    def update_count(self, length, count):
        if count < 0:
            return

        prev_count = self.counts[length]
        if count == prev_count:
            return
        
        count_diff = count - prev_count
        score_diff = game_config.length_values[length] * count_diff
        self.counts[length] = count
        self.control.update_count(length, count)
        self.update_train_score(self.train_score + score_diff)
        self.update_remaining(self.remaining - count_diff * length)

    def update_counts(self):
        for length, count in self.counts.items():
            self.control.update_count(length, count)

    def update_train_score(self, new_value):
        self.train_score = new_value
        self.control.update_train_score(new_value)
        self.update_total_score()

    def update_remaining(self, new_value):
        self.remaining = new_value
        text = new_value if new_value != game_config.remaining_pieces else None
        self.control.update_remaining(text)

    def update_total_score(self):
        longest_road_score = 10 if self.longest_road else 0
        ticket_score = self.ticket_score if self.ticket_score is not None else 0
        self.total_score = self.train_score + ticket_score + longest_road_score
        # print("Score for %s: %s = %s + %s + 10x%s" % (
        #     self.name, self.total_score, self.train_score, self.ticket_score, self.longest_road
        # ))
        if self.ticket_score is None or self.longest_road is None:
            self.control.update_total_score("?")
        else:
            self.control.update_total_score(self.total_score)

    def set_tickets_entered(self, text):
        self.tickets_entered = text

        if not text.strip():
            self.ticket_score = 0
            self.control.update_additional_total("")
            self.control.mark_additional_points_neutral()
            self.update_total_score()
            return

        pts = text.split()
        try:
            points = sum([int(pt) for pt in pts])
            self.update_ticket_score(points)
        except ValueError:
            self.ticket_score = None
            self.control.mark_additional_points_invalid()
            self.update_total_score()
            return "Could not parse " + text

    def update_ticket_score(self, new_value):
        self.ticket_score = new_value
        self.control.update_additional_total(new_value)
        self.control.mark_additional_points_valid()
        self.update_total_score()

    def set_longest_road(self, value):
        if value is None:
            if self.longest_road is None:
                return
        else:
            if self.longest_road == value and self.longest_road is not None:
                return

        self.longest_road = value
        self.control.set_has_longest_road(value)
        self.update_total_score()

    def set_longest_road_length_entered(self, value, force_update=False):
        # print("%s =?= %s" % (self.longest_road_length_entered, value, ))
        if self.longest_road_length_entered == value and not force_update:
            return

        self.longest_road_length_entered = value

        # print("'%s' is empty? %s" % (value, not value.strip()))
        if not value.strip():
            self.control.mark_longest_road_length_neutral()
            self.control.set_longest_road_length("")
            self.longest_road_length = 0
            return

        try:
            int_value = int(value)
        except ValueError:
            self.control.mark_longest_road_length_invalid()
            self.longest_road_length = None
            self.set_longest_road(None)
            return

        self.set_longest_road_length(int_value)
        self.control.mark_longest_road_length_valid()

    def set_longest_road_length(self, value):
        if self.longest_road_length == value:
            return

        self.longest_road_length = value
        self.control.set_longest_road_length(value)

    def set_name(self, new_name):
        self.name = new_name
        self.control.update_name(new_name)

    def update_all(self):
        self.control.update_color(self.color())
        self.control.update_name(self.name)
        self.update_counts()
        self.control.set_longest_road_length(self.longest_road_length_entered)
        self.set_longest_road_length_entered(self.longest_road_length_entered, True)
        self.control.set_has_longest_road(self.longest_road)
        self.control.set_tickets_entered(self.tickets_entered)
        self.set_tickets_entered(self.tickets_entered)
        self.control.update_additional_total(self.ticket_score)
        self.control.update_remaining(self.remaining)
        self.control.update_train_score(self.train_score)
        self.control.update_total_score(self.total_score)
        if self.is_minimized:
            self.control.minimize()
        else:
            self.control.restore()

    def minimize(self):
        self.is_minimized = True
        self.control.minimize()

    def restore(self):
        self.is_minimized = False
        self.control.restore()
