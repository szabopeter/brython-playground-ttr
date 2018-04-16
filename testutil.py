

class BrythonFunctionsMock:
    def __init__(self, validation):
        self.validation = validation

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

