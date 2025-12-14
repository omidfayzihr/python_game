from ui_helpers import alert
from combat import take_damage, combat


# Trap event - player slips and takes damage
def statue_slip():
    alert("⚠️ Oops!", "As you reach for the key, you slip on the polished floor!\n\nYou take 2 damage from the fall.")
    take_damage(2)


# Final boss fight with The Narrator
def narrator_boss_fight():
    alert("🎭 Final Confrontation",
          "A mysterious figure emerges from the shadows...\n\n"
          "\"So... you actually made it this far.\n"
          "Impressive. But can you defeat me?\"\n\n"
          "The Narrator prepares for battle!")
    combat("The Narrator", enemy_health=20, enemy_attack=5, enemy_armor=2)
