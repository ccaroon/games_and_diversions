#!/usr/bin/env python
import adventurelib
import random

from rune.realm import Realm
import rune.commands

# ------------------------------------------------------------------------------
# TODO: load realm
REALM = Realm("realms/grim-coast")
rune.commands.REALM = REALM
# TODO: load/init clock
# TODO: load character
# player = Character(f"")
# REALM.enter(player)
# TODO: load starting equipment
# TODO: load starting point
# TODO: export starting point
# ------------------------------------------------------------------------------
def prompt():
    return f"{REALM}> "
adventurelib.prompt = prompt

def invalid_command(cmd):
    print(random.choice([
        "Nothing happens.",
        "You shift from one foot to the other ... waiting."
    ]))
adventurelib.no_command_matches = invalid_command

# ------------------------------------------------------------------------------
REALM.intro()
adventurelib.start(help=True)
