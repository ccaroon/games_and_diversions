from rune.base import Base

class Point(Base):
    def __init__(self, path):
        super().__init__(path)

        self.__exits = self._data["travel"]

    def __str__(self):
        return f"==> {self.name} <==\n\n{self.flavor_text}"

    def exits(self):
        output = ""
        for exit_info in self.__exits:
            output += f"{exit_info['desc']} ({exit_info['name']})\n"

        return output
