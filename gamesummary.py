from controlid import ControlIdFactory, ControlId


class GameSummary:
    def __init__(self, brython_functions):
        self.players = []
        self.player_summaries = []
        self.control_id_factory = ControlIdFactory(brython_functions)

    def register(self, player):
        self.players.append(player)
        player_summary = PlayerSummary(len(self.player_summaries), self.control_id_factory)
        self.player_summaries.append(player_summary)

    def update_player(self, player):
        self.update()

    def update(self):
        self.players.sort(key=lambda p: p.total_score, reverse=True)
        for nr in range(len(self.players)):
            player = self.players[nr]
            player_summary = self.player_summaries[nr]
            player_summary.update(player)

    def clear(self):
        for player in self.players:
            player.player_summary = None

        self.players.clear()


class PlayerSummary:
    def __init__(self, nr, cif):
        self.nr = nr

        self.name = None
        self.score = None
        self.color = None

        assert isinstance(cif, ControlIdFactory)
        self.cif = cif
        self.CID_NAME = cif.create("player_summary_name", self.nr)
        self.CID_SCORE = cif.create("player_summary_score", self.nr)

    def update(self, player):
        if self.cif.is_valid() == False:
            return

        assert isinstance(self.CID_NAME, ControlId)
        assert isinstance(self.CID_SCORE, ControlId)

        if self.name != player.name:
            self.name = player.name
            self.CID_NAME.get().text = self.name

        if self.score != player.total_score:
            self.score = player.total_score
            self.CID_SCORE.get().text = self.score

        new_color = player.color()
        if self.color != new_color:
            self.color = new_color
            # TODO: html + cid
