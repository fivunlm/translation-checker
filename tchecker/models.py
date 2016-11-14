
class ResourceLocation:
    def __init__(self, file, line):
        self.file = file
        self.line = line

    def __eq__(self, location):
        return self.file == location.file and self.line == location.line


class TranslatableResource:
    def __init__(self, key):
        self.key = key
        self.locations = []

    def add_location(self, file, line):
        l = ResourceLocation(file, line)
        if l not in self.locations:
            self.locations.append(l)

    def __eq__(self, tr):
        return self.key == tr.key

    def __hash__(self):
        return hash(self.key)


class TranslatableResourceSet:
    def __init__(self):
        self._internal_list = []

    def append(self, tr):
        if tr in self._internal_list:
            for l in tr.locations:
                self._internal_list[self._internal_list.index(tr)].add_location(l.file, l.line)
        else:
            self._internal_list.append(tr)

    def __add__(self, other):
        # noinspection PyProtectedMember
        for tr in other._internal_list:
            self.append(tr)
        return self

    def __len__(self):
        return len(self._internal_list)

    def __iter__(self):
        for tr in self._internal_list:
            yield tr
