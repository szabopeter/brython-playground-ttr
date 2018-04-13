class ControlId:
    def __init__(self, brython_functions, prefix, args):
        self.brython_functions = brython_functions
        self.cid = prefix + "_".join([str(arg) for arg in args])

    def get(self):
        return self.brython_functions.get_element(self.cid)

    def is_valid(self):
        try:
            self.get()
            return True
        except KeyError:
            return False


class ControlIdFactory:
    def __init__(self, brython_functions, nr):
        self.nr = nr
        self.brython_functions = brython_functions
        self.created = []

    def create(self, prefix, *args):
        cid = ControlId(self.brython_functions, prefix, (self.nr, ) + args)
        self.created.append(cid)
        return cid

    def is_valid(self):
        missing = [cid.cid for cid in self.created if not cid.is_valid()]

        if len(missing) == 0:
            return True, None

        message = "Can't find required ids: {idlist}".format(idlist=", ".join(missing))
        return False, message


