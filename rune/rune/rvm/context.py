import pyparsing as pp

from scriptum.context import Context as ScriptumContext

class Context:

    __add = "add" + pp.QuotedString(quote_char='"')("name") + "with" + "icon" + pp.Char(pp.unicode.BMP.printables)("icon")
    # TODO: one_of
    __COMMANDS = (
        __add,
        "activate" + pp.Word(pp.alphanums)
    )

    @classmethod
    def parse(cls, command):
        result = None

        for cmd in cls.__COMMANDS:
            try:
                cmd.parse_string(command)
                break
            except pp.exceptions.ParseException as err:
                pass

    @classmethod
    @__add.set_parse_action
    def add(cls, result):
        ctx = ScriptumContext(result.name, icon=result.icon)

        # print(result)
        # print(result.name, result.icon)
        print(ctx)
