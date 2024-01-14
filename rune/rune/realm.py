import colorama

from rune.base import Base
from rune.point import Point

from scriptum.scene import Scene

class Realm(Base):
    def __init__(self, path):
        """
        Initialize a Realm

        Args:
            path (str): Path the the realm data file directory. Ex: realms/grim-coast
        """
        super().__init__(f"{path}/map.yml")

        self.__path = path
        self.__points = []
        self.__load_points()
        self.__current_location = self.__points[0]

        self.__init_intro()

    def __init_intro(self):
        self.__intro = Scene("Intro")
        self.__intro.add_dialogue(self.name, enlarge=True, color=colorama.Fore.LIGHTBLUE_EX)
        self.__intro.add_dialogue(self.flavor_text, color=colorama.Fore.LIGHTGREEN_EX)

    def __load_points(self, ):
        for pt_data in self._data["points"]:
            self.__points.append(Point(f"{self.__path}/points/{pt_data['name']}.yml"))

    def __str__(self):
        return f"{self.name}:{self.__current_location.name}"

    @property
    def current_location(self):
        return self.__current_location

    def set_location(self, point:Point):
        # TODO: iff possible to travel to point
        self.__current_location = Point

    def intro(self):
        self.__intro.play(clear_screen=True)




# scene = CutScene("Intro")
# scene.add_action(utils.clear_screen, pause=False)
# scene.add_dialogue("999",          enlarge=True, color=Fore.RED)
# scene.add_dialogue("Nine Hours",   enlarge=True, color=Fore.WHITE)
# scene.add_dialogue("Nine Persons", enlarge=True, color=Fore.WHITE)
# scene.add_dialogue("Nine Doors",   enlarge=True, color=Fore.RED)
# scene.add_dialogue("""
# Off in the murky, fog shrouded distance appears a cruise ship. It slowly turns broadside as it explodes in a fireball.
# """)
