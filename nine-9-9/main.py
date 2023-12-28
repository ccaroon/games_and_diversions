#!/usr/bin/env python
import adventurelib
import random

import contexts
from scriptum.context import Context

import commands
from scenes.intro import scene as intro

# ------------------------------------------------------------------------------
def prompt():
    if Context.ACTIVE:
        return F"999 - {Context.get()}> "
    else:
        return F"999> "
adventurelib.prompt = prompt

def invalid_command(cmd):
    print(random.choice([
        "Huh?",
        F"I don't know how to '{cmd}'",
        "Ummm...what?"
    ]))
adventurelib.no_command_matches = invalid_command

Context.add(contexts.CHEATING)
Context.add(contexts.LOCKED_IN)
# ------------------------------------------------------------------------------
intro.play()
adventurelib.start(help=True)
