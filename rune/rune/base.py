import yaml
class Base:
    def __init__(self, path):
        self._data = None
        with open(path, "r", encoding="utf-8") as fptr:
            self._data = yaml.safe_load(fptr)

    @property
    def name(self):
        return self._data["name"]

    @property
    def flavor_text(self):
        return self._data["flavor_text"]
