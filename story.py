import sys
from player import *
from combat import combat, take_damage, gain_experience
from ui_helpers import alert, ask_choice, ui_update_hud
from story_item import (add_golden_key_1, add_golden_key_2, add_amulet,
                        show_inventory_popup, has_both_keys, has_key_1, has_key_2)
from story_damage import narrator_boss_fight, statue_slip


def _hud():
    # Update HUD display with current stats
    ui_update_hud(player_name, player_class, player_health,
                  player_max_health, player_experience)


def start():
    # Start the game - wake up in the temple
    _hud()
    alert("👁️ Awakening",
          "You wake up slowly...\n\n"
          "Cold stone beneath your back. Darkness surrounds you.\n"
          "You hear only your own breathing echoing in the chamber.")

    opt = ask_choice("❓ What now?", "What do you want to do?",
                     ["👀 Look Around"])
    if opt == "👀 Look Around":
        start_area_intro()
    else:
        start()


def start_area_intro():
    # Describe the temple chamber and available doors
    _hud()
    alert("🏛️ Ancient Temple",
          "Your eyes adjust to the dim light...\n\n"
          "You're in an ancient temple chamber. An altar stands in the center, "
          "surrounded by old statues covered in dust.\n\n"
          "Two doors catch your attention:\n"
          "• A magnificent GOLDEN DOOR behind you\n"
          "• A heavy wooden EXIT door ahead")
    start_area_menu()


def start_area_menu():
    # Temple chamber menu - choose between golden door, exit, or statues
    _hud()
    options = ["🚪 Golden Door", "🚶 Exit Door", "🗿 Examine Statues"]

    opt = ask_choice("🏛️ Temple Chamber", "Where do you want to go?", options)

    if opt == "🚪 Golden Door":
        golden_door_check()
    elif opt == "🚶 Exit Door":
        exit_door()
    elif opt == "🗿 Examine Statues":
        statue_room()
    else:
        start_area_menu()


def golden_door_check():
    # Check if player has both keys and allow opening the door
    if has_both_keys():
        # Player has both keys - can open door
        alert("🔑 Keys Found!",
              "You have both Golden Keys!\n\n"
              "The keyholes glow with anticipation...")

        opt = ask_choice("🚪 Golden Door",
                         "Do you want to open the door?",
                         ["✅ Open Door", "🔍 Inspect", "⬅️ Back"])

        if opt == "✅ Open Door":
            open_golden_door()
        elif opt == "🔍 Inspect":
            alert("🔍 Inspection",
                  "Two ornate keyholes, perfectly matching your keys.\n\n"
                  "You're ready to open this door!")
            golden_door_check()
        else:
            start_area_menu()
    else:
        # Door locked - show which keys you have/need
        key_status = []
        if has_key_1():
            key_status.append("✅ Golden Key 1")
        else:
            key_status.append("❌ Golden Key 1")

        if has_key_2():
            key_status.append("✅ Golden Key 2")
        else:
            key_status.append("❌ Golden Key 2")

        alert("🔒 Locked",
              f"The golden door has two keyholes.\n\n"
              f"Keys needed:\n{key_status[0]}\n{key_status[1]}\n\n"
              f"You need BOTH keys to open this door.")

        opt = ask_choice("🚪 Golden Door",
                         "What do you want to do?",
                         ["🔍 Inspect", "⬅️ Back"])

        if opt == "🔍 Inspect":
            alert("🔍 Inspection",
                  f"Two keyholes carved into the golden door.\n\n"
                  f"Current status:\n{key_status[0]}\n{key_status[1]}")
            golden_door_check()
        else:
            start_area_menu()


def statue_room():
    # Investigate statues - triggers a trap but no actual key
    global statue_checked
    _hud()

    # If you already triggered the trap, nothing happens
    if statue_checked:
        alert("🗿 Statues",
              "The statues stand silently.\n\n"
              "Nothing else to find here...")
        start_area_menu()
        return

    alert("🗿 Statue Room",
          "You approach the statues...\n\n"
          "One statue - a priest - seems to be holding something golden.\n"
          "It looks like... a key?")

    opt = ask_choice("🗿 Statue", "What do you want to do?",
                     ["✋ Take Key", "⬅️ Back"])

    if opt == "✋ Take Key":
        statue_checked = True
        statue_slip()
        alert("😅 No Key", "There was no key after all... just a trick of the light.")
        start_area_menu()
    else:
        start_area_menu()


# Phase 6: Exit temple to outside world
def exit_door():
    # Exit the temple and go to the outside world
    _hud()
    alert("🚪 Exit Door",
          "An old wooden door with a surprisingly modern 'EXIT' sign.\n\n"
          "Light seeps through the cracks...")

    opt = ask_choice("🚪 Exit", "What do you want to do?",
                     ["🚶 Go Outside", "⬅️ Back"])

    if opt == "🚶 Go Outside":
        outside_intro()
    else:
        start_area_menu()


def outside_intro():
    # Describe the outside world and present path choices
    _hud()
    alert("☀️ Outside World",
          "You push the door open and step outside.\n\n"
          "Bright daylight! Fresh air! A forest surrounds the temple.\n\n"
          "Two paths branch out:\n"
          "• LEFT: A bridge over a flowing river\n"
          "• RIGHT: A small wooden hut in the trees")
    crossroads()


# Crossroads hub - dynamically show available paths
def crossroads():
    # Hub menu - choose between river path, forest path, or return to temple
    _hud()

    options = []

    # Only show paths that haven't been completed
    if not forest_finished:
        options.append("🏠 Hut Path")
    if not river_finished:
        options.append("🌊 River Path")

    # If both paths done, offer return to temple
    if river_finished and forest_finished:
        options.append("⬅️ Back to Temple")

    options.append("🎒 Inventory")

    # Display progress status
    progress = f"Progress: River {'✅' if river_finished else '❌'} | Forest {'✅' if forest_finished else '❌'}"

    opt = ask_choice("🌲 Crossroads", progress +
                     "\n\nWhere do you want to go?", options)

    if opt == "🏠 Hut Path":
        forest_path()
    elif opt == "🌊 River Path":
        river_path()
    elif opt == "⬅️ Back to Temple":
        return_to_temple()
    elif opt == "🎒 Inventory":
        show_inventory_popup()
        crossroads()
    else:
        crossroads()


def river_path():
    # River path - encounter old man, can fight or talk for first golden key
    _hud()

    if river_finished:
        alert("🌊 River", "You already completed this path.")
        crossroads()
        return

    alert("🌊 River Path",
          "You walk towards the bridge...\n\n"
          "An old man stands blocking your way, leaning on a walking stick.\n"
          "He looks at you with knowing eyes.")

    opt = ask_choice("👴 Old Man",
                     "The old man stands in your way. What do you do?",
                     ["⚔️ Attack", "💬 Talk", "⬅️ Back"])

    if opt == "⚔️ Attack":
        alert("⚔️ Combat!", "The old man grins...\n\n\"So be it, young one!\"")
        combat("Old Man", enemy_health=12, enemy_attack=4, enemy_armor=0)
        alert("🎁 Reward", "The old man drops something as he falls...\n\nA golden key!")
        add_golden_key_1()
        river_path_finished()
    elif opt == "💬 Talk":
        alert("💬 Conversation",
              "Old Man: \"Ah, a polite one! Rare these days.\"\n\n"
              "\"I have something you need... but first, a riddle!\"\n\n"
              "...\n\n"
              "\"Ah, never mind. I'm too old for this. Take the key!\"")
        add_golden_key_1()
        river_path_finished()
    else:
        crossroads()


def forest_path():
    # Forest path - fight goblin and collect second key and amulet
    _hud()

    if forest_finished:
        alert("🏠 Hut", "You already completed this path.")
        crossroads()
        return

    alert("🏠 Hut Path",
          "You approach the wooden hut...\n\n"
          "But before you reach it—\n\n"
          "A GOBLIN jumps out from behind a tree!\n"
          "\"GIVE ME YOUR GOLD!\" it screeches!")

    combat("Goblin", enemy_health=10, enemy_attack=5, enemy_armor=2)

    alert("🎁 Treasure!",
          "You search the goblin's belongings...\n\n"
          "You find:\n"
          "• A golden key\n"
          "• A mysterious amulet")

    add_golden_key_2()
    add_amulet()
    forest_path_finished()


# Mark river path complete - show progress
def river_path_finished():
    # Mark river path as complete and check if both paths done
    global river_finished
    river_finished = True
    _hud()

    alert("✅ River Path Complete",
          "You obtained Golden Key 1!\n\n"
          + ("Both keys collected! Return to the temple." if forest_finished else "One more path to explore..."))

    check_all_paths_done()


# Mark forest path complete - show progress
def forest_path_finished():
    # Mark forest path as complete and check if both paths done
    global forest_finished
    forest_finished = True
    _hud()

    alert("✅ Forest Path Complete",
          "You obtained Golden Key 2!\n\n"
          + ("Both keys collected! Return to the temple." if river_finished else "One more path to explore..."))

    check_all_paths_done()


# Check if both paths are complete - advance to next phase
def check_all_paths_done():
    # If both paths complete, return to temple; otherwise go to crossroads
    if river_finished and forest_finished:
        show_inventory_popup()
        opt = ask_choice("🎉 All Paths Complete!",
                         "You have both golden keys!\n\nReturn to the temple?",
                         ["✅ Yes, Go Back", "🎒 Check Inventory"])
        if opt == "🎒 Check Inventory":
            show_inventory_popup()
            check_all_paths_done()
        else:
            return_to_temple()
    else:
        crossroads()


# Return to temple after both paths complete
def return_to_temple():
    # Return to temple after completing both outside paths
    _hud()
    alert("🏛️ Return",
          "You make your way back to the ancient temple...\n\n"
          "The golden door awaits.")
    start_area_menu()


# Phase 8: Final sequence - open the golden door
def open_golden_door():
    # Open golden door and face The Narrator in final boss fight
    _hud()

    alert("🔓 Opening...",
          "You insert both golden keys into the keyholes...\n\n"
          "*Click*\n\n"
          "The door glows brightly and swings open!")

    alert("👁️ Beyond the Door",
          "You step through into a dark chamber...\n\n"
          "A single spotlight illuminates a figure in the center.")

    narrator_boss_fight()
    ending()


# Final ending scene - congratulations and stats summary
def ending():
    # Display final victory message with player stats
    _hud()

    alert("🏆 Victory!",
          "The Narrator falls to their knees...\n\n"
          "\"Impressive... You've truly earned your freedom.\"\n\n"
          "The temple begins to shake...")

    # Compile inventory list for display
    inv_items = []
    for item in player_inventory:
        if isinstance(item, dict):
            inv_items.append(item['name'])
        else:
            inv_items.append(str(item))
    inv_text = ', '.join(inv_items) if inv_items else 'Nothing'

    alert("🎮 THE END",
          f"Congratulations, {player_name}!\n\n"
          f"━━━━━━━ FINAL STATS ━━━━━━━\n"
          f"Class: {player_class}\n"
          f"Origin: {player_origin}\n"
          f"Health: {player_health}/{player_max_health}\n"
          f"XP Earned: {player_experience}\n"
          f"Items: {inv_text}\n\n"
          f"You have completed the adventure!\n\n"
          f"Thanks for playing! 🎉")

    sys.exit()
