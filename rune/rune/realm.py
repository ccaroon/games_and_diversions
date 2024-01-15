import colorama

from rune.base import Base
from rune.point import Point

from scriptum.context import Context
from scriptum.scene import Scene

class Realm(Base):
    def __init__(self, path):
        """
        Initialize a Realm

        Args:
            path (str): Path the the realm data file directory. Ex: realms/grim-coast
        """
        super().__init__(f"{path}/realm.yml")

        self.__path = path
        self.__load_points()
        self.__init_intro()
        self.__init_clocks()

    def __init_clocks(self):
        # TODO: implement
        for clock in self._data["clocks"]:
            pass


    def __init_intro(self):
        self.__intro = Scene("Intro")
        self.__intro.add_dialogue(self.name, enlarge=True, color=colorama.Fore.LIGHTBLUE_EX)
        self.__intro.add_dialogue(self.flavor_text, color=colorama.Fore.LIGHTGREEN_EX)

    def __load_points(self):
        self.__points = {}
        for pt_data in self._data["points"]:
            self.__points[pt_data["name"]] = Point(f"{self.__path}/points/{pt_data['name']}.yml")

        self.__starting_point = self.point(self._data["points"][0]["name"])

    def __str__(self):
        return f"{self.name}"

    def intro(self):
        self.__intro.play(clear_screen=True)

    @property
    def starting_point(self):
        return self.__starting_point

    def point(self, name):
        return self.__points.get(name)


#
