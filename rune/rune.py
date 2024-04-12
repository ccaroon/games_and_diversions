#!/usr/bin/env python
"""
A Virtual Tabletop for Rune By Spencer Campbell & Published by Gila RPGs (gilarpgs.com)
"""
import argparse
import random

import adventurelib

from rune.rvm.rvm import RVM

from rune.character import Character
from rune.realm import Realm
import rune.commands

# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description='RUNE - A solo tabletop roleplaying game. By Spencer Campbell. Published by Gila RPGs (gilarpgs.com).'
)
# parser.set_defaults(func=usage, app=parser)
parser.add_argument("realm", type=str)
parser.add_argument("character", type=str)
args = parser.parse_args()
# ------------------------------------------------------------------------------
# import sys
# val = RVM.parse('context --> add "day" with icon ☀️')
# print(val)
# sys.exit(0)

# ------------------------------------------------------------------------------
# Realm
realm = Realm(args.realm)
rune.commands.REALM = realm

# TODO: load/init clock

# Character
player = Character(args.character)
rune.commands.PLAYER = player
player.enter(realm)

# TODO: load starting equipment
# ------------------------------------------------------------------------------
def prompt():
    return f"{player}> "
adventurelib.prompt = prompt

def invalid_command(cmd):
    print(random.choice([
        "Nothing happens.",
        "You shift from one foot to the other ... waiting."
    ]))
adventurelib.no_command_matches = invalid_command

# ------------------------------------------------------------------------------
realm.intro()
rune.commands.look()
adventurelib.start(help=True)
