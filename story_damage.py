# story_damage.py - Damage events and special encounters
from ui_helpers import alert
from combat import take_damage, combat

def statue_slip():
    """Player slips while trying to grab the key from the statue"""
    alert("⚠️ Oops!", "As you reach for the key, you slip on the polished floor!\n\nYou take 2 damage from the fall.")
    take_damage(2)

def narrator_boss_fight():
    """Final boss fight with the Narrator"""
    alert("🎭 Final Confrontation",
          "A mysterious figure emerges from the shadows...\n\n"
          "\"So... you actually made it this far.\n"
          "Impressive. But can you defeat me?\"\n\n"
          "The Narrator prepares for battle!")
    combat("The Narrator", enemy_health=20, enemy_attack=5, enemy_armor=2)