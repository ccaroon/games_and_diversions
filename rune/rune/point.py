from rune.base import Base

class Point(Base):
    def __init__(self, path):
        super().__init__(path)

        self.__init_actions()
        self.__init_travel()

    def __str__(self):
        return f"==> {self.name} <==\n\n{self.flavor_text}"

    def __init_actions(self):
        self.__actions = self._data["actions"]
        # self.__actions = {}
        # for name, data in self._data["actions"].items():
        #     self.__actions[name] = data

    def __init_travel(self):
        self.__paths = []
        for point in self._data["travel"]:
            self.__paths.append(point["name"])

    def can(self, action):
        # TOOD: apply restrictions
        #   when: day | night
        #   fights resloved?
        #   etc...
        return action in self.__actions

    def has_path_to(self, name):
        return name in self.__paths

    def actions(self):
        output = ""
        for name, action in self.__actions.items():
            output += f"--> {name}: {action['when']}\n"
        return output

    def exits(self):
        output = ""
        for exit_info in self._data["travel"]:
            output += f"{exit_info['desc']} ({exit_info['name']})\n"

        return output
