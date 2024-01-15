""" Rune Virtual Machine?! """

from rune.rvm.context import Context

class RVM:
    __PARSERS = {
        "context": Context
    }

    @classmethod
    def get(cls, name):
        return cls.__PARSERS.get(name)
