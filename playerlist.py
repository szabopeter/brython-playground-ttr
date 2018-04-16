class PlayerList:
    def __init__(self, players):
        self.players = players[:]
        self.saved_order = None
        self.saved_minimizations = None
        self.can_save = True

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        class PlayerListIterator:
            def __init__(self, players):
                self.current = 0
                self.players = players

            def __next__(self):
                try:
                    self.current += 1
                    return self.players[self.current-1]
                except IndexError:
                    raise StopIteration

        return PlayerListIterator(self.players)

    def __getitem__(self, index):
        return self.players[index]

    def sort(self, key, reverse):
        controls = [p.control for p in self.players]
        self.players.sort(key=key, reverse=reverse)

        for i in range(len(controls)):
            player = self.players[i]
            if player.control != controls[i]:
                player.control = controls[i]
                player.update_all()

    def get_players(self):
        return self.players

    def finish(self):
        self.sort(key=lambda p: p.total_score, reverse=True)

    def minimize_and_move_to_last(self, player_moving):
        controls = [p.control for p in self.players]
        self.players.remove(player_moving)
        self.players.append(player_moving)

        for i in range(len(controls)):
            player = self.players[i]
            if player.control != controls[i]:
                player.control = controls[i]
                player.update_all()

        player_moving.minimize()
        self.save_order()

    def restore_and_move_up(self, player_moving):
        controls = [p.control for p in self.players]
        self.players.remove(player_moving)

        for i in range(len(self.players)):
            if self.players[i].is_minimized:
                self.players.insert(i, player_moving)
                break

        if player_moving not in self.players:
            self.players.append(player_moving)

        for i in range(len(controls)):
            player = self.players[i]
            if player.control != controls[i]:
                player.control = controls[i]
                player.update_all()

        player_moving.restore()
        self.save_order()

    def restart(self):
        self.load_order()
        self.can_save = True
        for player in self.players:
            player.reset()

    def save_order(self):
        if not self.can_save:
            return

        self.saved_order = self.players[:]
        self.saved_minimizations = [player.is_minimized for player in self.players]

    def load_order(self):
        if self.saved_order is None or self.saved_minimizations is None:
            return

        controls = [p.control for p in self.players]

        self.players = self.saved_order[:]

        for i in range(len(controls)):
            player = self.players[i]
            need_update = False

            if player.is_minimized != self.saved_minimizations[i]:
                player.is_minimized = self.saved_minimizations[i]
                need_update = True

            if player.control != controls[i]:
                player.control = controls[i]
                need_update = True

            if need_update:
                player.update_all()

    def is_valid(self):
        for player in self.players:
            valid, message = player.control.is_valid()
            if not valid:
                return False, message

        return True, None

