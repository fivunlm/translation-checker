
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

    def __eq__(self, key):
        return self.key == key

    def __hash__(self):
        return hash(self.key)
