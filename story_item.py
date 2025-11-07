# story_item.py - Inventory management
from player import *
from ui_helpers import alert


def has_both_keys():
    """Check if player has both golden keys"""
    has_key1 = "Golden Key 1" in player_inventory
    has_key2 = "Golden Key 2" in player_inventory
    return has_key1 and has_key2


def has_key_1():
    """Check if player has golden key 1"""
    return "Golden Key 1" in player_inventory


def has_key_2():
    """Check if player has golden key 2"""
    return "Golden Key 2" in player_inventory


def add_golden_key_1():
    """Add golden key 1 to inventory"""
    if "Golden Key 1" not in player_inventory:
        player_inventory.append("Golden Key 1")
        alert("🔑 Item Found", "You obtained: Golden Key 1")


def add_golden_key_2():
    """Add golden key 2 to inventory"""
    if "Golden Key 2" not in player_inventory:
        player_inventory.append("Golden Key 2")
        alert("🔑 Item Found", "You obtained: Golden Key 2")


def add_amulet():
    """Add amulet to inventory"""
    if not any(isinstance(i, dict) and i.get("name") == "Amulet" for i in player_inventory):
        player_inventory.append({"name": "Amulet", "desc": "An ancient amulet radiating mysterious power."})
        alert("✨ Item Found", "You obtained: Amulet\nAn ancient amulet radiating mysterious power.")


def show_inventory_popup():
    """Show inventory in a popup"""
    if not player_inventory:
        alert("🎒 Inventory", "Your inventory is empty.\n\nExplore the world to find items!")
        return

    lines = ["Your current items:\n"]
    for item in player_inventory:
        if isinstance(item, dict):
            lines.append(f"  🔹 {item.get('name')}: {item.get('desc', '')}")
        else:
            lines.append(f"  🔹 {item}")

    alert("🎒 Inventory", "\n".join(lines))