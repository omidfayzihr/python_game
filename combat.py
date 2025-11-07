# combat.py - Combat system
import random
import sys
from player import *
from ui_helpers import ask_choice, ui_update_hud, alert


def take_damage(amount):
    """Player takes damage"""
    global player_health
    player_health -= amount
    if player_health <= 0:
        player_health = 0
        ui_update_hud(player_name, player_class, player_health, player_max_health, player_experience)
        alert("💀 Defeated", f"You have been defeated...\n\nYour adventure ends here, {player_name}.")
        sys.exit()
    ui_update_hud(player_name, player_class, player_health, player_max_health, player_experience)


def gain_experience(amount):
    """Player gains experience"""
    global player_experience
    player_experience += amount
    ui_update_hud(player_name, player_class, player_health, player_max_health, player_experience)


def combat(enemy_name, enemy_health, enemy_attack, enemy_armor):
    """Turn-based combat system"""
    max_enemy_health = enemy_health
    alert("⚔️ Combat Started", f"{player_name} vs {enemy_name}\n\nEnemy HP: {enemy_health}/{max_enemy_health}")
    ui_update_hud(player_name, player_class, player_health, player_max_health, player_experience)

    turn = 1
    while enemy_health > 0 and player_health > 0:
        # Player turn
        choice = ask_choice(
            f"⚔️ Turn {turn} - Your Action",
            f"Your HP: {player_health}/{player_max_health}\nEnemy HP: {enemy_health}/{max_enemy_health}\n\nWhat will you do?",
            ["⚔️ Attack", "🛡️ Defend"]
        )

        defending = False

        if choice == "⚔️ Attack":
            # Calculate damage
            damage_dealt = player_attack + player_strength - enemy_armor
            if damage_dealt < 0:
                damage_dealt = 0

            # Hit chance (80%)
            if random.randint(1, 100) > 20:
                enemy_health -= damage_dealt
                if enemy_health < 0:
                    enemy_health = 0
                alert("💥 Hit!",
                      f"You strike {enemy_name} for {damage_dealt} damage!\n\nEnemy HP: {enemy_health}/{max_enemy_health}")
            else:
                alert("💨 Miss!", f"Your attack misses {enemy_name}!")

        elif choice == "🛡️ Defend":
            defending = True
            alert("🛡️ Defending", "You brace yourself and prepare to block the next attack!")

        # Check if enemy is defeated
        if enemy_health <= 0:
            alert("🏆 Victory!", f"You defeated {enemy_name}!\n\n+5 XP")
            gain_experience(5)
            break

        # Enemy turn
        enemy_damage = enemy_attack - player_armor
        if defending:
            enemy_damage = enemy_damage // 2
        if enemy_damage < 1:
            enemy_damage = 1

        # Dodge chance
        if random.randint(1, 100) > player_dodge:
            take_damage(enemy_damage)
            alert("💢 Enemy Attack!",
                  f"{enemy_name} hits you for {enemy_damage} damage!\n\nYour HP: {player_health}/{player_max_health}")
        else:
            alert("💨 Dodged!", f"You dodge {enemy_name}'s attack!")

        turn += 1