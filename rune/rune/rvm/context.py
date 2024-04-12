import pyparsing as pp

from scriptum.context_manager import ContextManager

class Context:

    __add = "add" + pp.QuotedString(quote_char='"')("name") + "with" + "icon" + pp.Char(pp.unicode.BMP.printables)("icon")
    __activate = "activate" + pp.QuotedString(quote_char='"')("name")

    __COMMANDS = (
        __add,
        __activate
    )

    @classmethod
    def parse(cls, command):
        result = None

        for cmd in cls.__COMMANDS:
            try:
                result = cmd.parse_string(command)
                break
            except pp.exceptions.ParseException as err:
                result = None

        if result == None:
            raise ValueError(f"context -> Invalid Command: `{command}`")

        return result[0]

    @classmethod
    @__add.set_parse_action
    def add(cls, result):
        ctx = ContextManager.create(result.name, icon=result.icon)
        return ctx

    @classmethod
    @__activate.set_parse_action
    def activate(cls, result):
         ctx = ContextManager.get(result.name)
         ContextManager.activate(ctx)









#
