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

    def is_valid(self):
        return self.control_id_factory.is_valid()


class PlayerSummary:
    def __init__(self, nr, cif):
        self.nr = nr

        self.name = None
        self.score = None
        self.color = None
        self.is_minimized = None

        assert isinstance(cif, ControlIdFactory)
        self.cif = cif
        self.CID_NAME = cif.create("player_summary_name", self.nr)
        self.CID_SCORE = cif.create("player_summary_score", self.nr)
        self.CID_PLAYER = cif.create("player_summary", self.nr)

    def update(self, player):
        assert isinstance(self.cif, ControlIdFactory)

        valid, _ = self.cif.is_valid()
        if not valid:
            return

        assert isinstance(self.CID_NAME, ControlId)
        assert isinstance(self.CID_SCORE, ControlId)
        assert isinstance(self.CID_PLAYER, ControlId)

        if self.name != player.name:
            self.name = player.name
            self.CID_NAME.get().text = self.name

        if self.score != player.total_score:
            self.score = player.total_score
            self.CID_SCORE.get().text = self.score

        new_color = player.color()
        # print("Change color: {old} -> {new}".format(old=self.color, new=new_color))
        if self.color != new_color:
            if self.color is not None:
                css_class = "player_color_{color}".format(color=self.color)
                self.cif.brython_functions.remove_class(self.CID_PLAYER.cid, css_class)

            self.color = new_color
            css_class = "player_color_{color}".format(color=self.color)
            self.cif.brython_functions.add_class(self.CID_PLAYER.cid, css_class)

        if self.is_minimized != player.is_minimized:
            self.is_minimized = player.is_minimized
            if self.is_minimized:
                self.cif.brython_functions.hide(self.CID_PLAYER.cid)
            else:
                self.cif.brython_functions.show(self.CID_PLAYER.cid)
