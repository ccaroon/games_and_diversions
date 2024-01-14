from rune.base import Base
from rune.realm import Realm

from scriptum.inventory import Inventory

class Character(Base):
    def __init__(self, path):
        super().__init__(path)

        self.__health = self._data["health"]
        self.__harm = self._data["harm"]
        self.__stamina = self._data["stamina"]
        self.__lore = self._data["lore"]

        self.__realm = None
        self.__point = None

        self.__save_data = self._data.get("save_data", {})

    @property
    def point(self):
        return self.__point

    def enter(self, realm:Realm):
        if realm.name != self.__save_data.get("realm"):
            # Reset Lore if entering new realm
            self.__lore = 0

        self.__realm = realm
        self.__point = realm.point(self.__save_data.get("point"))
        if not self.__point:
            self.__point = realm.starting_point

    def rest(self):
        self.__harm = 0
        # TODO: reset fights

    def travel(self, name):
        travel_ok = False
        if self.__point.has_path_to(name):
            self.__point = self.__realm.point(name)
            travel_ok = True

        return travel_ok

    def save(self):
        # TODO: implement
        pass

    def stats(self):
        return f"""* Health: {self.__health - self.__harm}/{self.__health}
* Stamina: {self.__stamina}
* Lore: {self.__lore}
"""

    def __str__(self):
        return f"{self.name}@{self.__realm.name}:{self.__point.name}"








#
