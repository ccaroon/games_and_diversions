""" Rune Virtual Machine?! """

from rune.rvm.context import Context

class RVM:
    __PARSERS = {
        "context": Context
    }

    @classmethod
    def get(cls, name):
        return cls.__PARSERS.get(name)

    @classmethod
    def parse(cls, rvm_cmd):
        (parser_name, cmd) = rvm_cmd.split("->", 2)

        # print(f"[{parser_name}] . [{cmd}]")
        parser = cls.get(parser_name.strip())
        result = parser.parse(cmd.strip())

        return result
