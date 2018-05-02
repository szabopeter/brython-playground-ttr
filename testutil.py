from gameconfig import game_config
from playercontrol import PlayerControl


class BrythonFunctionsMock:
    def __init__(self, validation):
        self.validation = validation

    def hide(self, _):
        pass

    def show(self, _):
        pass

    @staticmethod
    def using_idlist(*valid_ids):
        def validation(eid):
            return eid in valid_ids

        return BrythonFunctionsMock(validation)

    @staticmethod
    def accepting_anything():
        return BrythonFunctionsMock(lambda eid: True)

    def get_element(self, eid):
        if self.validation(eid):
            return ElementMock(eid)

        raise KeyError()


class ElementMock:
    def __init__(self, eid):
        def nop(_):
            pass

        self.text = eid
        self.value = eid
        self.classList = ClassListMock()


class ClassListMock:
    def add(self, _):
        pass

    def remove(self, _):
        pass


def create_player_control_mock(nr=0):
    brython_functions = BrythonFunctionsMock.accepting_anything()
    return PlayerControl(nr, game_config, brython_functions)
