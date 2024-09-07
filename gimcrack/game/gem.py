class Gem:
    def __init__(self, icon, color):
        self.__icon = icon
        self.__color = color


    @property
    def icon(self):
        return self.__icon


    @property
    def color(self):
        return self.__color


    def __str__(self) -> str:
        return f"<{self.__icon}>({self.__color})"


    def __repr__(self) -> str:
        return f"Gem({self.__icon}, {self.__color})"


    def __eq__(self, other: object) -> bool:
        return repr(self) == repr(other)
