# game.py
# Week 1 – SAMENGEVOEGDE WERKENDE VERSIE (Omid + Justin)
# Opzet: 1 bestand met Omid’s basis (stats/combat/flow) + Justin’s teksten waar ze horen.
# Alleen minimale fixes voor werkende code. Geen refactors.

import tkinter
from tkinter import messagebox, simpledialog
import sys
import random

# =========================
#         GLOBALS
# =========================
# -- Omid --
player_name = ""
player_class = ""
player_origin = ""

player_health = 12
player_max_health = 12

player_strength = 0
player_armor = 0
player_dodge = 0
player_attack = 0
player_experience = 0
player_inventory = []

river_finished = False
forest_finished = False


# =========================
#   HELPER / UI (tkinter)
# =========================
# -- Justin (welcome popup) --
def welcome_popup():
    """Laat een welkomstmelding zien en vraag of speler door wil."""
    root = tkinter.Tk()
    root.withdraw()
    choice = messagebox.askquestion(
        "Welcome",
        "🎮 Welcome to the Adventure Text-Based Game!\n\n"
        "You wake up in a strange place... "
        "Your choices will decide your fate.\n\n"
        "Do you have the courage to continue?"
    )
    if choice != "yes":
        print("You turn back before the journey even begins...")
        return False
    root.destroy()
    return True


# -- Justin (naam) --
def ask_name():
    """Vraag naam via dialog"""
    global player_name
    root = tkinter.Tk()
    root.withdraw()
    name = simpledialog.askstring("Character Creation", "What is your name, adventurer?")
    player_name = name if name else "Unknown Hero"
    root.destroy()


# -- Omid (klasse) + Justin (teksten) --
def choose_class():
    """Kies class via klein GUI-venster"""
    global player_class, player_health, player_max_health, player_strength, player_armor, player_dodge, player_attack

    root = tkinter.Tk()
    root.withdraw()
    win = tkinter.Toplevel()
    win.title("Choose Your Class")
    win.geometry("400x300")

    tkinter.Label(win, text="Choose Your Class:", font=("Arial", 14, "bold")).pack(pady=10)
    tkinter.Label(win, text="⚔️ Warrior - High armor and health, strong attacks", font=("Arial", 10)).pack(pady=5)
    tkinter.Label(win, text="🔮 Mage - Powerful magic, low defense", font=("Arial", 10)).pack(pady=5)
    tkinter.Label(win, text="🗡️ Rogue - High dodge, balanced stats", font=("Arial", 10)).pack(pady=5)

    def select_warrior():
        nonlocal win
        # -- Omid default stats (laag getal range) --
        set_stats("Warrior", hp=12, max_hp=12, str_=15, arm=20, ddg=5, atk=10)
        win.destroy()

    def select_mage():
        nonlocal win
        set_stats("Mage", hp=8, max_hp=8, str_=8, arm=5, ddg=10, atk=20)
        win.destroy()

    def select_rogue():
        nonlocal win
        set_stats("Rogue", hp=10, max_hp=10, str_=12, arm=10, ddg=20, atk=15)
        win.destroy()

    tkinter.Button(win, text="Warrior", width=15, bg="#8B0000", fg="white", command=select_warrior).pack(pady=5)
    tkinter.Button(win, text="Mage", width=15, bg="#4B0082", fg="white", command=select_mage).pack(pady=5)
    tkinter.Button(win, text="Rogue", width=15, bg="#2F4F2F", fg="white", command=select_rogue).pack(pady=5)

    win.wait_window()
    root.destroy()


def set_stats(klass, hp, max_hp, str_, arm, ddg, atk):
    global player_class, player_health, player_max_health, player_strength, player_armor, player_dodge, player_attack
    player_class = klass
    player_health = hp
    player_max_health = max_hp
    player_strength = str_
    player_armor = arm
    player_dodge = ddg
    player_attack = atk


# -- Justin (herkomst) --
def ask_origin():
    global player_origin
    root = tkinter.Tk()
    root.withdraw()
    origin = simpledialog.askstring("Character Origin", "Where do you come from?\n(e.g., Village, Mountains, City)")
    player_origin = origin if origin else "Unknown Lands"
    root.destroy()


# -- Justin + Omid (stats tonen) --
def show_stats():
    root = tkinter.Tk()
    root.withdraw()
    stats_text = f"""
📊 Character Stats:

Name: {player_name}
Class: {player_class}
Origin: {player_origin}

❤️ Health: {player_health}/{player_max_health}
💪 Strength: {player_strength}
🛡️ Armor: {player_armor}
🏃 Dodge: {player_dodge}
⚔️ Attack: {player_attack}
⭐ Experience: {player_experience}
"""
    messagebox.showinfo("Your Character", stats_text)
    root.destroy()


# =========================
#     COMBAT / DAMAGE
# =========================
# -- Omid --
def take_damage(amount):
    global player_health
    player_health -= amount
    if player_health <= 0:
        player_health = 0
        print("\n💀 You have died... Game Over!")
        sys.exit()
    print(f"❤️ Current Health: {player_health}/{player_max_health}")


# -- Justin calls this soms; daarom toevoegen --
def check_health():
    """Compat: Justin riep check_health() aan na zelf health aanpassen."""
    if player_health <= 0:
        print("Game Over!")
        print("(Man you are good at failing)")
        sys.exit()


# -- Omid --
def gain_experience(amount):
    global player_experience
    player_experience += amount
    print(f"⭐ You gained {amount} experience! Total: {player_experience}")


# -- Omid combat (basic) --
def combat(enemy_name, enemy_health, enemy_attack, enemy_armor):
    print(f"\n⚔️ COMBAT START: {player_name} vs {enemy_name}!")
    print(f"Enemy Health: {enemy_health}")
    print(f"Your Health: {player_health}/{player_max_health}\n")

    while enemy_health > 0 and player_health > 0:
        print("--- Your Turn ---")
        print("A) Attack")
        print("B) Defend (reduce incoming damage)")
        choice = input("> ").lower()

        defending = False
        if choice == "a":
            damage_dealt = player_attack + player_strength - enemy_armor
            if damage_dealt < 0:
                damage_dealt = 0
            hit_chance = random.randint(1, 100)
            if hit_chance > 20:
                enemy_health -= damage_dealt
                print(f"💥 You hit {enemy_name} for {damage_dealt} damage!")
                print(f"Enemy Health: {enemy_health}\n")
            else:
                print("💨 You missed!\n")
        elif choice == "b":
            print("🛡️ You brace yourself for the enemy attack!\n")
            defending = True
        else:
            print("Invalid choice! You hesitate...\n")

        if enemy_health <= 0:
            print(f"🎉 Victory! You defeated {enemy_name}!")
            gain_experience(5)
            break

        print("--- Enemy Turn ---")
        enemy_damage = enemy_attack - player_armor
        if defending:
            enemy_damage //= 2
        if enemy_damage < 1:
            enemy_damage = 1

        dodge_chance = random.randint(1, 100)
        if dodge_chance > player_dodge:
            take_damage(enemy_damage)
            print(f"💢 {enemy_name} hits you for {enemy_damage} damage!")
        else:
            print("💨 You dodged the attack!")
        print()


# =========================
#        STORY / FLOW
# =========================
# -- Justin (intro-tekst) + Omid (flowkeuzes) --
def start():
    print("")
    print("You awaken to the sound of your own breath, sharp and unsteady. "
          "The chill of cold stone presses against your back, sending a shiver through you. "
          "Blinking away the haze of sleep, you slowly become aware of your surroundings.")
    print("")
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
    print("You lie upon what seems to be an altar—hard, unyielding, and carved from grey stone.")
    print("As your eyes adjust to the dim light, you begin to see the chamber around you: "
          "statues, old carvings, and two paths—one heavy door ahead, and a golden door behind.")
    start_area_without_intro()


def start_area_without_intro():
    print("")
    print("Well where do you want to go?")
    print("A) Go to the golden door behind you.")
    print("B) Go to the door in front of you.")
    print("C) Go to the statues.")
    c = input("> ").lower()
    if c == "a":
        A_golden_door_1()
    elif c == "b":
        exit_door()
    elif c == "c":
        statue_room()
    else:
        print("")
        print("Invalid choice. Try again.")
        start_area_without_intro()


def A_golden_door_1():
    print("")
    print("Step by step, you draw nearer to the golden, intricately carved door. "
          "With each movement, the air grows heavier.")
    print("")
    print("What do you want to do?")
    print("A) Open the door.")
    print("B) Inspect the door.")
    print("C) Go back.")
    c = input("> ").lower()
    if c == "a":
        A_open_the_door_1()
    elif c == "b":
        B_inspect_door_1()
    elif c == "c":
        C_go_back_golden_door_1()
    else:
        print("Invalid choice. Try again.")
        A_golden_door_1()


def A_open_the_door_1():
    print("")
    print("It's locked.")
    A_golden_door_1()


def B_inspect_door_1():
    print("")
    print("As you look at the door, you notice there are two keyholes.")
    print("Somehow? I am as confused as you.")
    print("Maybe you need to find both keys to open it.")
    A_golden_door_1()


def C_go_back_golden_door_1():
    print("")
    print("You return to the altar.")
    start_area_without_intro()


# -- Justin (statue room + damage gag) --
def no_morals():
    global player_health
    print("")
    print("As you climb up to grab the key, it's stuck. On the way down you slip.")
    print("Good job… [You have taken 2 damage]")
    player_health -= 2
    check_health()
    print(f"[You have {player_health} health remaining]")
    print("You exit the statue room and return to the altar.")
    start_area_without_intro()


def statue_room():
    print("")
    print("You step into the statue room...")
    print("Do you want to look around?")
    print("A) Sure why not.")
    c = input("> ").lower()
    if c == "a":
        statue_part_2()
    else:
        print("Invalid choice. Try again.")
        statue_room()


def statue_part_2():
    print("")
    print("One statue stands out: a priestly figure holding a key.")
    print("")
    print("What do you want to do?")
    print("A) Keep your morals and go back.")
    print("B) Become a filthy criminal and take the key.")
    c = input("> ").lower()
    if c == "a":
        start_area_without_intro()
    elif c == "b":
        no_morals()
    else:
        print("Invalid choice. Try again.")
        statue_part_2()


# -- Justin (exit deur / buiten) --
def exit_door():
    print("")
    print("You approach a door under a big red neon sign saying 'EXIT'.")
    print("What do you want to do?")
    print("A) Inspect the exit door.")
    print("B) Go outside. (you can't go back after going outside)")
    print("C) Go back to the altar.")
    c = input("> ").lower()
    if c == "a":
        exit_inspect()
    elif c == "b":
        outside_with_text()
    elif c == "c":
        start_area_without_intro()
    else:
        print("Invalid choice. Try again.")
        exit_door()


def exit_inspect():
    print("")
    print("Old wooden door, weathered and splintered, with a hyper-modern 'EXIT' sign above it.")
    exit_door()


def outside_with_text():
    print("")
    print("You step outside: bright daylight, a forest all around.")
    print("Do you want to take a look around?")
    print("A) Yes")
    print("B) No")
    c = input("> ").lower()
    if c == "a":
        outside_yes()
    elif c == "b":
        outside_no_1()
    else:
        print("Invalid choice. Try again.")
        outside_with_text()


def outside_no_1():
    print("")
    print("You don't want to look around? Uhm… sure.")
    print("Soooo... you still wanna look around?")
    print("A) Yes")
    print("B) Don't feel like it")
    c = input("> ").lower()
    if c == "a":
        outside_yes()
    elif c == "b":
        outside_no_2()
    else:
        print("Invalid choice. Try again.")
        outside_no_1()


def outside_no_2():
    print("")
    print("Skipping context already? Bold strategy.")
    print("C'mon.. go take a look around please?")
    print("A) Yes")
    print("B) Not really")
    c = input("> ").lower()
    if c == "a":
        outside_yes()
    elif c == "b":
        outside_no_3()
    else:
        print("Invalid choice. Try again.")
        outside_no_2()


def outside_no_3():
    print("")
    print("\033[1mThe choice isn't yours to make.\033[0m")
    print("Look around.")
    print("A) Yes")
    print("B) Yes")
    c = input("> ").lower()
    if c in ("a", "b"):
        outside_yes()
    else:
        print("Invalid choice. Try again.")
        outside_no_3()


def outside_yes():
    print("")
    print("To your left: a dirt road to a bridge over the river.")
    print("To your right: a narrow path toward a wooden hut.")
    outside_yes_without_text()


def outside_yes_without_text():
    print("")
    print("So… bridge or creepy hut? Your move.")
    print("A) To the hut we go!")
    print("B) River path sounds safe")
    c = input("> ").lower()
    if c == "a":
        forest_path()
    elif c == "b":
        river_path()
    else:
        print("Invalid choice. Try again.")
        outside_yes_without_text()


# --------- RIVER PATH (Justin + Omid) ---------
def river_path():
    print("As you stroll along the river path, behold—water!")
    print("An old man yells from the bridge.")
    print(f"'Traveler, who has chosen the mighty path of {player_class}—{player_name}!' the old man shouts.")
    print('"I wish to play a game with you!" (He said that very rudely, by the way.)')
    print("")
    print("Wanna hear an old and rude man yap?")
    print("A) Attack for no reason (RPG experience!)")
    print("B) Hear him out.")
    c = input("> ").lower()
    if c == "a":
        battle_oldman()
    elif c == "b":
        hear_oldman_out()
    else:
        print("Invalid choice. Try again.")
        river_path()


def battle_oldman():
    # -- Omid (echte simpele combat) --
    combat("Old Man", enemy_health=15, enemy_attack=3, enemy_armor=0)
    after_battle_oldman()


def after_battle_oldman():
    print("\nWHY EVEN HE WAS A NICE OLD MAN?")
    print("WHAT DID HE DO? HE WAS HARMLESS???")
    print("You know what, fine—take some damage.")
    take_damage(2)
    not_feel_guilty()


def hear_oldman_out():
    print("")
    print("Upon closer inspection, the old man looks about as threatening as a damp towel.")
    oldman_explain_riddle()


def not_feel_guilty():
    print("")
    print("At the end of the bridge, you find a chest. You didn't earn this; there was a riddle planned. :(")
    chest_choice()


def oldman_explain_riddle():
    print("")
    print('Oh, good stranger! "It’s quite simple—just a riddle!"')
    print("He smiles: 'I am practicing for my grandson! Gotta keep my wits sharp!'")
    print("")
    print("Are you up for a riddle?")
    print("A) Sure, why not")
    print("B) Be an ass and refuse")
    c = input("> ").lower()
    if c == "a":
        doing_riddle()
    elif c == "b":
        being_an_ass()
    else:
        print("Invalid choice. Try again.")
        oldman_explain_riddle()


def doing_riddle():
    print("")
    print("The riddle goes as follows:")
    print("What goes up but never comes down?")
    print("(Hint: 3 letters.)")
    ans = input("> ").lower()
    if ans == "age":
        guess_right_1()
    else:
        guess_wrong_1()


def guess_right_1():
    print("")
    print("Wow, you're good at this! the old man says, impressed.")
    guess_final()


def guess_wrong_1():
    print("")
    print("Wrong. Hint: the word begins with the letter A.")
    ans = input("> ").lower()
    if ans == "age":
        guess_right_2()
    else:
        guess_wrong_2()


def guess_right_2():
    print('"Good job!" the old man says cheerfully.')
    guess_semi_final()


def guess_wrong_2():
    print('"He gave you a hint—how did you still fail?" the old man mocks.')
    print("Another hint: It has an A and G.")
    ans = input("> ").lower()
    if ans == "age":
        guess_right_3()
    else:
        guess_wrong_3()


def guess_right_3():
    print('"Good job!" the old man says happily.')
    guess_semi_final()


def guess_wrong_3():
    print('"He gave you a hint—how did you still fail?" the old man asks.')
    print("Last hint: The word is age.. (come on)")
    ans = input("> ").lower()
    if ans == "age":
        guess_right_4()
    else:
        guess_wrong_4()


def guess_right_4():
    print('"Good job!" the old man says (finally).')
    guess_semi_final()


def guess_wrong_4():
    print('"Are you quite alright?" the old man asks genuinely.')
    print("Free will is too much responsibility for you.")
    print("A) Age.")
    ans = input("> ").lower()
    if ans == "a":
        guess_semi_final()
    else:
        print("Invalid choice. Try again.")
        guess_wrong_4()


def guess_semi_final():
    print("I should be on my way now. These legs aren't what they used to be.")
    guess_final()


def guess_final():
    chest_choice()


def being_an_ass():
    print("")
    print("You walk away. The old man stumbles... SPLASH.")
    print("You gain 2 experience points. (Yikes.)")
    gain_experience(2)
    not_feel_guilty()


def chest_choice():
    print("Open the chest?")
    print("A) Why not")
    c = input("> ").lower()
    if c == "a":
        chest_river_after()
    else:
        print("Invalid choice. Try again.")
        chest_choice()


def chest_river_after():
    print("Inside the chest, you find a key.")
    player_inventory.append("Golden Key 1")
    print("(You are done with this area.)")
    river_path_finished()


# --------- FOREST / HUT (Justin + Omid) ---------
def forest_path():
    print("A goblin jumps out from the bushes!")
    goblin_fight()


def goblin_fight():
    # In Justin’s versie zat (nog) geen echte combat; Omid had er wel één.
    combat("Goblin", enemy_health=8, enemy_attack=4, enemy_armor=2)
    forest_path_2()


def forest_path_2():
    print("Further along the path you find a door that needs a word code.")
    galgje()


def galgje():
    word = "doorknob"
    guessed = []
    tries = 7
    while tries > 0:
        out = "".join([ch if ch in guessed else "_" for ch in word])
        print(out)
        if "_" not in out:
            print("")
            print("(You are great at going oogabooga at puzzles.)")
            hut()
            return
        guess = input("Guess a letter: ").lower()
        if guess in word and guess not in guessed:
            guessed.append(guess)
        else:
            tries -= 1
            print("(man you are not good at guessing)")
            print(f"You still got {tries} tries left.")
    print("Game over! Let's try that again.")
    galgje()


def hut():
    print("You enter a dusty hut. There is a chest.")
    print("A) Open the chest")
    c = input("> ").lower()
    if c == "a":
        chest_open()
    else:
        print("Invalid choice. Try again.")
        hut()


def chest_open():
    print("You found a totally unimportant key.")
    player_inventory.append("Golden Key 2")
    dick_move_hut()


def dick_move_hut():
    print("For no apparent reason… pick a number for me?")
    v = input("> ")
    if v.isdigit():
        dmg = int(v)
        print(f"[You have taken {dmg} damage]")
        take_damage(dmg)
        petty()
    else:
        print("yeah no you aren't funny pick one.")
        not_entertained()


def not_entertained():
    print("")
    print("You aren't being funny—pick one.")
    v = input("> ")
    if v.isdigit():
        dmg = int(v)
        print(f"[You have taken {dmg} damage]")
        take_damage(dmg)
        petty()
    else:
        print("yeah no you aren't funny—fine.")
        punishment_hut()


def petty():
    print("I was feeling petty lol.")
    final_hut()


def punishment_hut():
    print("[You have taken 3 damage]")
    take_damage(3)
    final_hut()


def final_hut():
    print("(You are done with this area.)")
    forest_path_finished()


# --------- ROUTE MANAGEMENT (Justin) ---------
def river_path_finished():
    global river_finished
    print("You reach the end of the river path.")
    river_finished = True
    go_to_next_route()


def forest_path_finished():
    global forest_finished
    print("You leave the forest path.")
    forest_finished = True
    go_to_next_route()


def go_to_next_route():
    if not river_finished:
        riverpath_second_route()
    elif not forest_finished:
        forestpath_second_route()
    else:
        go_to_final_place()


def riverpath_second_route():
    print("Back at the crossroads. Only one way left.")
    print("A) River path sounds safe.")
    c = input("> ").lower()
    if c == "a":
        river_path()
    else:
        print("Invalid choice. Try again.")
        riverpath_second_route()


def forestpath_second_route():
    print("Back at the crossroads. Only one way left.")
    print("A) To the hut we go!")
    c = input("> ").lower()
    if c == "a":
        forest_path()
    else:
        print("Invalid choice. Try again.")
        forestpath_second_route()


def go_to_final_place():
    print("The curiosity must be killing you. Let's go back..")
    print("A) Yeah let's go to the golden door in the temple.")
    c = input("> ").lower()
    if c == "a":
        golden_door_final()
    else:
        print("Invalid choice. Try again.")
        go_to_final_place()


def golden_door_final():
    print("You step back inside; the golden door gleams.")
    print("Open the door?")
    print("A) Yes.")
    c = input("> ").lower()
    if c == "a":
        inside_golden_door()
    else:
        print("Invalid choice. Try again.")
        golden_door_final()


def inside_golden_door():
    print("You slide the keys into the golden door.")
    print("(Yes, all of them—nothing says 'epic moment' like jingling metal in a sacred lock.)")
    print("It swings open, and the first thing you see is an…")
    print("A) I don't see it—get out of the way!")
    c = input("> ").lower()
    if c == "a":
        demo_ending()
    else:
        print("Invalid choice. Try again.")
        inside_golden_door()


def demo_ending():
    print(f"\nCongratulations, {player_name}! You didn't die.")
    print("You made it through the chaos, traps, mockery and questionable choices.")
    print("\nFinal Stats:")
    print(f"❤️ Health: {player_health}/{player_max_health}")
    print(f"⭐ Experience: {player_experience}")
    print(f"🎒 Inventory: {', '.join(player_inventory) if player_inventory else 'Nothing!'}")
    print("\nThank you for playing!\n")
    sys.exit()


# =========================
#          MAIN
# =========================
if __name__ == "__main__":
    if welcome_popup():
        ask_name()
        choose_class()
        ask_origin()
        show_stats()
        print(f"\n✅ {player_name} the {player_class} from {player_origin} is ready for adventure!\n")
        input("Press ENTER to begin your journey...")
        start()
