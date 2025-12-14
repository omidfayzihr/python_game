from player import *
from ui_helpers import alert


# Check if player has both required keys
def has_both_keys():
    has_key1 = "Golden Key 1" in player_inventory
    has_key2 = "Golden Key 2" in player_inventory
    return has_key1 and has_key2


# Check if player has first key
def has_key_1():
    return "Golden Key 1" in player_inventory


# Check if player has second key
def has_key_2():
    return "Golden Key 2" in player_inventory


# Add first key to inventory (prevent duplicates)
def add_golden_key_1():
    if "Golden Key 1" not in player_inventory:
        player_inventory.append("Golden Key 1")
        alert("🔑 Item Found", "You obtained: Golden Key 1")


# Add second key to inventory (prevent duplicates)
def add_golden_key_2():
    if "Golden Key 2" not in player_inventory:
        player_inventory.append("Golden Key 2")
        alert("🔑 Item Found", "You obtained: Golden Key 2")


# Add special amulet item with description (prevent duplicates)
def add_amulet():
    if not any(isinstance(i, dict) and i.get("name") == "Amulet" for i in player_inventory):
        player_inventory.append(
            {"name": "Amulet", "desc": "An ancient amulet radiating mysterious power."})
        alert("✨ Item Found",
              "You obtained: Amulet\nAn ancient amulet radiating mysterious power.")


# Display inventory popup - shows all items collected
def show_inventory_popup():
    if not player_inventory:
        alert("🎒 Inventory",
              "Your inventory is empty.\n\nExplore the world to find items!")
        return

    lines = ["Your current items:\n"]
    for item in player_inventory:
        if isinstance(item, dict):
            lines.append(f"  🔹 {item.get('name')}: {item.get('desc', '')}")
        else:
            lines.append(f"  🔹 {item}")

    alert("🎒 Inventory", "\n".join(lines))
