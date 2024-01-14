from adventurelib import *

# TODO: commands
# fight
# search
# check clock
# rest
# inventory

REALM = None
PLAYER = None

# ------------------------------------------------------------------------------
# Game
# ------------------------------------------------------------------------------
@when("save")
def save_state():
    say("Saving has not yet been implemented!")
# ------------------------------------------------------------------------------
# Inventory Related Commands
# ------------------------------------------------------------------------------
# @when("i")
# @when("inventory")
# def view():
#     if INVENTORY:
#         print(F"You're carrying {len(INVENTORY)} items:")
#         for item in INVENTORY:
#             print(F"{item} - {item.isa}")
#     else:
#         print("You have nothing!")

# @when("examine THING")
# @when("x THING")
# @when("look at THING")
# def examine(thing):
#     item = INVENTORY.find(thing)
#     if not item:
#         item = CURRENT_ROOM.objects.find(thing)

#     if item:
#         say(item.describe())
#     else:
#         say(F"You don't have any {thing}.")
# ------------------------------------------------------------------------------
@when("l")
@when("look")
def look():
    print(PLAYER.point)
    print(PLAYER.point.actions())
    print(PLAYER.point.exits())

@when("stats")
def show_player_stats():
    # TODO: show weapons
    # TODO: show gear
    # TODO: show rune
    # TODO: show inventory
    # TODO: similar to player sheet
    print(PLAYER.stats())

@when("travel POINT")
@when("move to POINT")
def travel(point):
    if PLAYER.travel(point):
        look()
    else:
        print(f"You can't get to {point} from here!")

@when("rest")
def rest():
    if PLAYER.point.can("rest"):
        PLAYER.rest()
        print("You feel refreshed!")
        show_player_stats()
    else:
        print("You can't rest here!")

@when("map")
def map():
    say("Sure would be nice to have a map of this place.")

# ------------------------------------------------------------------------------
# Cheating
# ------------------------------------------------------------------------------
# @when("context ACTION", context="cheating")
# def context(action):
#     if action == "clear":
#         Context.clear()
#         Context.add(contexts.CHEATING)
#     elif action == "show":
#         print(get_context())
#     elif action.startswith("add"):
#         status = action.replace("add", "")
#         ctx = Context(status.strip())
#         Context.add(ctx)

# @when("cheat ACTION", context="cheating")
# def cheat(action):
#     print(F"Unknown cheat command '{action}'.")









#
