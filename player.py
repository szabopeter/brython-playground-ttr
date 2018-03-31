from gameconfig import game_config


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

    def color(self):
        return game_config.all_colors[self.color_nr]

    def increase_count(self, length):
        self.update_count(length, self.counts[length] + 1)

    def decrease_count(self, length):
        self.update_count(length, self.counts[length] - 1)

    def update_count(self, length, count):
        prev_count = self.counts[length]
        if count == prev_count:
            return
        
        count_diff = count - prev_count
        score_diff = game_config.length_values[length] * count_diff
        self.counts[length] = count
        self.control.update_count(length, count)
        self.update_train_score(self.train_score + score_diff)
        self.update_remaining(self.remaining - count_diff * length)

    def update_train_score(self, new_value):
        self.train_score = new_value
        self.control.update_train_score(new_value)
        self.update_total_score()

    def update_remaining(self, new_value):
        self.remaining = new_value
        self.control.update_remaining(new_value)

    def update_total_score(self):
        self.total_score = self.train_score + self.ticket_score
        self.control.update_total_score(self.total_score)

    def update_ticket_score(self, new_value):
        self.ticket_score = new_value
        self.control.update_additional_total(new_value)
        self.control.mark_additional_points_valid()
        self.update_total_score()

