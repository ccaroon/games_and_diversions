class Clock:
    TYPE_CYCLICAL = "cyclical"
    TYPE_SINGULAR = "singular"

    def __init__(self, name, type, segments, effect, triggers):
        self.__name = name

        self.__type = type.lower()
        if self.__type not in (self.TYPE_CYCLICAL, self.TYPE_SINGULAR):
            raise ValueError(f"{name} -> {type} is not a valid Realm Clock type.")

        self.__segments = segments
        self.__segment_count = 0

        self.__effect = effect
        self.__triggers = triggers

    def tick(self):
        self.__segment_count += 1
        if self.__segment_count > self.__segments:
            # TODO: apply effect
            self.__apply_effect()
            # TODO: reset seg cnt if cyclical
            if self.__type == self.TYPE_CYCLICAL:
                self.__segment_count = 0

    def __apply_effect(self):
        pass

    def __str__(self):
        return f"{self.__name}: {self.__segment_count}/{self.__segments}"

    # def __tick_cyclical(self):
    #     pass

    # def __tick_singular(self):
    #     pass
