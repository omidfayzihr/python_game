# combat.py
# Hier staan alle functies voor gevechten en schade.

import random
import sys
from player import *

def take_damage(amount):
    global player_health
    player_health -= amount
    if player_health <= 0:
        player_health = 0
        print("\n💀 You have died... Game Over!")
        sys.exit()
    print(f"❤️ Current Health: {player_health}/{player_max_health}")


def gain_experience(amount):
    global player_experience
    player_experience += amount
    print(f"⭐ You gained {amount} experience! Total: {player_experience}")


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
