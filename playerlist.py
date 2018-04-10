class PlayerList:
    def __init__(self, players):
        self.players = players[:]

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