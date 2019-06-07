from adventurelib import *

import lib.contexts as contexts

from lib.context import Context
from lib.inventory import INVENTORY
from lib.map import CURRENT_ROOM

# ------------------------------------------------------------------------------
# Game
# ------------------------------------------------------------------------------
@when("save")
def save_state():
    say("Saving has not yet been implemented!")
# ------------------------------------------------------------------------------
# Inventory Related Commands
# ------------------------------------------------------------------------------
@when("i")
@when("inventory")
def view():
    if INVENTORY:
        print(F"You're carrying {len(INVENTORY)} items:")
        for item in INVENTORY:
            print(F"{item} - {item.isa}")
    else:
        print("You have nothing!")

@when("pick up THING", action="pickup")
@when("search for THING", action="search")
@when("take THING", action="take")
def add_item(thing, action):
    item = CURRENT_ROOM.items.take(thing)
    if action == "search":
        if item:
            INVENTORY.add(item)
            say(F"Your thorough and diligent searching has lead the discovery of {item}")
        else:
            say(F"Your thorough and diligent searching has been for naught. You can't find {thing}.")
    else:
        if item:
            INVENTORY.add(item)
            print(F"You take the {thing}.")
        else:
            say(F"You don't see any {thing} here.")

@when("drop THING")
def remove_item(thing):
    item = INVENTORY.take(thing)
    if item:
        CURRENT_ROOM.items.add(item)
        say(F"Dropped {thing}.")
    else:
        say(F"You're not even carrying a {thing}.")

@when("examine THING")
@when("x THING")
@when("look at THING")
def examine(thing):
    item = INVENTORY.find(thing)
    if not item:
        item = CURRENT_ROOM.objects.find(thing)

    if item:
        if item.desc:
            say(item.desc)
        else:
            say(item)
        
        if item.state:
            say(F"It's {item.state}.")
    else:
        say(F"You don't have any {thing}.")
# ------------------------------------------------------------------------------
# Room Related Commands
# ------------------------------------------------------------------------------
@when("l")
@when("look")
def look():
    print(CURRENT_ROOM)

    # TODO: better incorporate items in to the narrative
    if CURRENT_ROOM.items:
        print("\nLooking around you reveals: ")
        for thing in CURRENT_ROOM.items:
            print(thing)

    # TODO: better incorporate exits in to the narrative
    exits = CURRENT_ROOM.exits()
    if exits:
        print(F"\nExits: {exits}")

@when("map")
def map():
    say("Sure would be nice to have a map of this place.")
# ------------------------------------------------------------------------------
# Movement
# ------------------------------------------------------------------------------
@when("exit")
def leave():
    global CURRENT_ROOM

    if contexts.LOCKED_IN.is_active():
        say("You're locked in!")
    else:
        exits = CURRENT_ROOM.exits()
        if len(exits) > 1:
            say(F"""
                There's more than one way to leave this room. Which one would you like to try?
                {exits}
            """)
        else:
            CURRENT_ROOM = CURRENT_ROOM.exit(exits[0])

@when('n', direction='north')
@when('e', direction='east')
@when('s', direction='south')
@when('w', direction='west')
def move(direction):
    global CURRENT_ROOM

    if contexts.LOCKED_IN.is_active():
        say("You're locked in!")
    else:
        room = CURRENT_ROOM.exit(direction)
        if room:
            CURRENT_ROOM = room
            print(CURRENT_ROOM)
        else:
            print(F"You can't move {direction}.")
# ------------------------------------------------------------------------------
# Cheating
# ------------------------------------------------------------------------------
@when("context ACTION", context="cheating")
def context(action):
    if action == "clear":
        Context.clear()
        Context.add(contexts.CHEATING)
    elif action == "show":
        print(get_context())
    elif action.startswith("add"):
        status = action.replace("add", "")
        ctx = Context(status.strip())
        Context.add(ctx)

@when("cheat ACTION", context="cheating")
def cheat(action):
    print(F"Unknown cheat command '{action}'.")









# 
