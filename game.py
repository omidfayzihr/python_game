# main.py
# Dit is het startpunt van de game.

from ui_helpers import welcome_popup, ask_name, choose_class, ask_origin, show_stats
from story import start
from player import player_name, player_class, player_origin

if __name__ == "__main__":
    if welcome_popup():
        ask_name()
        choose_class()
        ask_origin()
        show_stats()
        print(f"\n✅ {player_name} the {player_class} from {player_origin} is ready for adventure!\n")
        input("Press ENTER to begin your journey...")
        start()
