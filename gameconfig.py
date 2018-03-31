

class GameConfig:
    def __init__(self):
        
        self.max_players = 5
        self.all_colors = "red green blue yellow black".split()


        self.length_values = {
            1: 1,
            2: 2,
            3: 4,
            4: 7,
            5: 10,
            6: 15,
            7: 25,
            }

        self.remaining_pieces = 45
        self.train_lengths = [1, 2, 3, 4, 5, 6]


game_config = GameConfig()

