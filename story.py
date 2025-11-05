# story.py
# Alle verhaalfuncties en keuzes staan hier.

import sys
from player import *
from combat import combat, take_damage, gain_experience

def start():
    print("")
    print("You awaken to the sound of your own breath, sharp and unsteady...")
    print("What do you do?")
    print("A) Look around.")
    choice = input("> ").lower()
    if choice == "a":
        start_area_intro()
    else:
        print("Invalid choice. Try again.")
        start()


def start_area_intro():
    print("")
    print("You lie upon what seems to be an altar—hard and carved from grey stone.")
    print("You see statues, carvings, and two paths—one heavy door ahead, and a golden door behind.")
    start_area_without_intro()


def start_area_without_intro():
    print("")
    print("Where do you want to go?")
    print("A) Golden door behind you.")
    print("B) Door in front of you.")
    print("C) Statues.")
    c = input("> ").lower()
    if c == "a":
        golden_door()
    elif c == "b":
        exit_door()
    elif c == "c":
        statue_room()
    else:
        print("Invalid choice. Try again.")
        start_area_without_intro()


def golden_door():
    print("")
    print("You approach the golden door. It looks ancient and heavy.")
    print("It's locked.")
    start_area_without_intro()


def exit_door():
    print("")
    print("You walk toward a door under a red neon sign saying 'EXIT'.")
    print("A) Go outside.")
    print("B) Go back.")
    c = input("> ").lower()
    if c == "a":
        outside()
    else:
        start_area_without_intro()


def statue_room():
    print("")
    print("You step into the statue room. One statue holds a key.")
    print("A) Take the key.")
    print("B) Go back.")
    c = input("> ").lower()
    if c == "a":
        print("You slip and take 2 damage.")
        take_damage(2)
        start_area_without_intro()
    else:
        start_area_without_intro()


def outside():
    print("")
    print("You step into bright daylight. A path leads to a river and another to a hut.")
    print("A) River path.")
    print("B) Hut path.")
    c = input("> ").lower()
    if c == "a":
        river_path()
    elif c == "b":
        hut_path()
    else:
        print("Invalid choice.")
        outside()


def river_path():
    print("An old man stands by a bridge.")
    print("A) Talk to him.")
    print("B) Attack him.")
    c = input("> ").lower()
    if c == "b":
        combat("Old Man", 10, 3, 0)
        gain_experience(5)
        print("You find a golden key on him.")
        start_area_without_intro()
    else:
        print("He greets you kindly and gives you a riddle instead.")
        start_area_without_intro()


def hut_path():
    print("A goblin appears!")
    combat("Goblin", 8, 4, 1)
    gain_experience(5)
    print("You found another key!")
    start_area_without_intro()
