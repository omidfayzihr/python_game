# game.py - Entry point and character creation
from player import *
from ui_helpers import welcome_popup, ask_text, alert, ask_choice, ui_init, ui_update_hud
from story import start


def _refresh():
    """Update the HUD"""
    ui_update_hud(player_name, player_class, player_health, player_max_health, player_experience)


def ask_name_loop():
    """Ask for player name with validation"""
    global player_name

    while True:
        n = ask_text("👤 Character Name", "What is your character's name?\n\n(This will be your hero's identity)")

        if n and len(n.strip()) > 0:
            player_name = n.strip()
            break

        # No name entered
        pick = ask_choice(
            "❌ No Name?",
            "You didn't enter a name. What would you like to do?",
            ["Use 'Unknown Hero'", "Enter Again"]
        )

        if pick == "Use 'Unknown Hero'":
            player_name = "Unknown Hero"
            break


def choose_class():
    """Choose character class with stats"""
    global player_class, player_health, player_max_health, player_strength, player_armor, player_dodge, player_attack

    alert("🎭 Choose Your Class",
          "Each class has unique strengths and weaknesses.\n\n"
          "Choose wisely - this will affect your entire journey!")

    while True:
        opt = ask_choice(
            "🎭 Character Class",
            "Select your class:",
            [
                "⚔️ Warrior (High HP & Armor)",
                "🔮 Mage (Powerful Magic Attacks)",
                "🗡️ Rogue (High Dodge & Critical)"
            ]
        )

        if opt is None:
            continue

        def set_stats(klass, hp, max_hp, str_, arm, ddg, atk):
            global player_class, player_health, player_max_health, player_strength, player_armor, player_dodge, player_attack
            player_class = klass
            player_health = hp
            player_max_health = max_hp
            player_strength = str_
            player_armor = arm
            player_dodge = ddg
            player_attack = atk

        if opt.startswith("⚔️"):
            set_stats("Warrior", 15, 15, 15, 20, 5, 10)
            alert("⚔️ Warrior Selected",
                  "You are now a Warrior!\n\n"
                  "HP: 15 | Armor: 20 | Attack: 10\n"
                  "Strength: 15 | Dodge: 5")
        elif opt.startswith("🔮"):
            set_stats("Mage", 10, 10, 8, 5, 10, 20)
            alert("🔮 Mage Selected",
                  "You are now a Mage!\n\n"
                  "HP: 10 | Armor: 5 | Attack: 20\n"
                  "Strength: 8 | Dodge: 10")
        elif opt.startswith("🗡️"):
            set_stats("Rogue", 12, 12, 12, 10, 25, 15)
            alert("🗡️ Rogue Selected",
                  "You are now a Rogue!\n\n"
                  "HP: 12 | Armor: 10 | Attack: 15\n"
                  "Strength: 12 | Dodge: 25")
        else:
            continue

        _refresh()
        return


def choose_origin():
    """Choose character origin"""
    global player_origin

    alert("🌍 Choose Your Origin",
          "Where does your story begin?\n\n"
          "Your origin shapes who you are.")

    while True:
        opt = ask_choice(
            "🌍 Character Origin",
            "Where are you from?",
            ["🏘️ Village", "⛰️ Mountains", "🏛️ City", "✍️ Custom..."]
        )

        if opt == "🏘️ Village":
            player_origin = "Village"
            alert("🏘️ Village Origin",
                  "You grew up in a peaceful village,\n"
                  "learning the ways of the common folk.")
            return
        elif opt == "⛰️ Mountains":
            player_origin = "Mountains"
            alert("⛰️ Mountain Origin",
                  "You were raised in the harsh mountains,\n"
                  "making you tough and resilient.")
            return
        elif opt == "🏛️ City":
            player_origin = "City"
            alert("🏛️ City Origin",
                  "You come from a bustling city,\n"
                  "street-smart and quick-witted.")
            return
        elif opt == "✍️ Custom...":
            val = ask_text("✍️ Custom Origin",
                           "Enter your custom origin:\n\n"
                           "(e.g., 'Distant Kingdom', 'Lost Island', etc.)")
            if val and len(val.strip()) > 0:
                player_origin = val.strip()
                alert("✍️ Custom Origin", f"Your origin: {player_origin}\n\nA unique and mysterious background!")
                return
            else:
                alert("❌ Invalid", "Please enter a valid origin or choose from the list.")


def show_stats():
    """Show final character stats"""
    _refresh()
    alert("📊 Character Created",
          f"Name: {player_name}\n"
          f"Class: {player_class}\n"
          f"Origin: {player_origin}\n\n"
          f"━━━━━━━ STATS ━━━━━━━\n"
          f"❤️ Health: {player_health}/{player_max_health}\n"
          f"💪 Strength: {player_strength}\n"
          f"🛡️ Armor: {player_armor}\n"
          f"💨 Dodge: {player_dodge}%\n"
          f"⚔️ Attack: {player_attack}\n"
          f"⭐ XP: {player_experience}\n\n"
          f"Ready for adventure!")


if __name__ == "__main__":
    # Initialize UI
    ui_init()

    # Welcome screen
    if not welcome_popup():
        leave = ask_choice(
            "❌ Quit Game?",
            "Are you absolutely sure you want to quit?",
            ["Start Game Anyway", "Yes, Quit"]
        )
        if leave == "Yes, Quit":
            import sys

            sys.exit(0)

    # Character creation flow
    ask_name_loop()
    _refresh()

    choose_class()
    _refresh()

    choose_origin()
    _refresh()

    show_stats()

    # Start the adventure
    alert("🎮 Adventure Begins",
          "Your journey starts now...\n\n"
          "Press OK to begin!")

    start()