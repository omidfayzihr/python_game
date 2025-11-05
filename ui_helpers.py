# ui_helpers.py
# Alle kleine functies voor invoer, keuzes en vensters.

import tkinter
from tkinter import messagebox, simpledialog
from player import *

def welcome_popup():
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


def ask_name():
    global player_name
    root = tkinter.Tk()
    root.withdraw()
    name = simpledialog.askstring("Character Creation", "What is your name, adventurer?")
    player_name = name if name else "Unknown Hero"
    root.destroy()


def choose_class():
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

    def set_stats(klass, hp, max_hp, str_, arm, ddg, atk):
        global player_class, player_health, player_max_health, player_strength, player_armor, player_dodge, player_attack
        player_class = klass
        player_health = hp
        player_max_health = max_hp
        player_strength = str_
        player_armor = arm
        player_dodge = ddg
        player_attack = atk

    def select_warrior():
        set_stats("Warrior", hp=12, max_hp=12, str_=15, arm=20, ddg=5, atk=10)
        win.destroy()

    def select_mage():
        set_stats("Mage", hp=8, max_hp=8, str_=8, arm=5, ddg=10, atk=20)
        win.destroy()

    def select_rogue():
        set_stats("Rogue", hp=10, max_hp=10, str_=12, arm=10, ddg=20, atk=15)
        win.destroy()

    tkinter.Button(win, text="Warrior", width=15, bg="#8B0000", fg="white", command=select_warrior).pack(pady=5)
    tkinter.Button(win, text="Mage", width=15, bg="#4B0082", fg="white", command=select_mage).pack(pady=5)
    tkinter.Button(win, text="Rogue", width=15, bg="#2F4F2F", fg="white", command=select_rogue).pack(pady=5)

    win.wait_window()
    root.destroy()


def ask_origin():
    global player_origin
    root = tkinter.Tk()
    root.withdraw()
    origin = simpledialog.askstring("Character Origin", "Where do you come from?\n(e.g., Village, Mountains, City)")
    player_origin = origin if origin else "Unknown Lands"
    root.destroy()


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
