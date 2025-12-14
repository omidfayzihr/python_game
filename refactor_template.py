

# ============================================================================
# CLASS 1: PLAYER player.py
# ============================================================================


class Player:
    """Player class - alles wat je van een speler moet weten"""

    def __init__(self, name, player_class, origin, max_health=100):
        # Basic info
        self.name = name
        self.player_class = player_class
        self.origin = origin

        # Stats
        self.health = max_health
        self.max_health = max_health
        self.experience = 0

        # Inventory
        self.inventory = []
        self.golden_key_1 = False
        self.golden_key_2 = False
        self.amulet = False

    def take_damage(self, damage):
        """Damage system"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return self.health

    def heal(self, amount):
        """Healing"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def gain_experience(self, xp):
        """Get XP"""
        self.experience += xp

    def add_item(self, item):
        """Add item to inventory"""
        self.inventory.append(item)

    def has_both_keys(self):
        """Check for both keys"""
        return self.golden_key_1 and self.golden_key_2

    def is_alive(self):
        """Check if player is alive"""
        return self.health > 0


# ============================================================================
# CLASS 2: ENEMY enemy.py
# ============================================================================

class Enemy:
    """Enemy class - any enemy in the game"""

    def __init__(self, name, health, attack_power, armor=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.armor = armor

    def take_damage(self, damage):
        """Apply damage to enemy"""
        actual_damage = max(1, damage - self.armor)
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0
        return actual_damage

    def attack(self, target):
        """Attack the target (usually player)"""
        import random
        hit_chance = 0.8  # 80% hit rate

        if random.random() < hit_chance:
            damage = self.attack_power
            target.take_damage(damage)
            return damage
        else:
            return 0  # Miss

    def is_defeated(self):
        """Check if enemy is dead"""
        return self.health <= 0


# ============================================================================
# CLASS 3: COMBAT combat.py
# ============================================================================

class Combat:
    """Combat system - handles fights between player and enemy"""

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def player_attack(self):
        """Player turn"""
        import random
        damage = random.randint(10, 20)
        actual_damage = self.enemy.take_damage(damage)
        return actual_damage

    def enemy_turn(self):
        """Enemy turn"""
        damage = self.enemy.attack(self.player)
        return damage

    def run_combat(self):
        """Run full combat loop"""
        while self.player.is_alive() and not self.enemy.is_defeated():
            # Player attacks
            p_damage = self.player_attack()
            print(f"Player deals {p_damage} damage!")

            if self.enemy.is_defeated():
                break

            # Enemy attacks
            e_damage = self.enemy_turn()
            print(f"Enemy deals {e_damage} damage!")

            if not self.player.is_alive():
                break

        # Return result
        if self.player.is_alive():
            self.player.gain_experience(50)
            return "victory"
        else:
            return "defeat"


# ============================================================================
# CLASS 4: GAME game.py
# ============================================================================

class Game:
    """Main game class - orchestrates everything"""

    def __init__(self):
        self.player = None
        self.is_running = False

    def create_player(self, name, player_class, origin):
        """Create player during character creation"""
        self.player = Player(name, player_class, origin)
        print(
            f"Player created: {self.player.name} the {self.player.player_class}")

    def start_combat(self, enemy_name, enemy_health, enemy_attack, enemy_armor=0):
        """Start a combat encounter"""
        enemy = Enemy(enemy_name, enemy_health, enemy_attack, enemy_armor)
        combat = Combat(self.player, enemy)
        result = combat.run_combat()
        return result

    def game_over(self):
        """End game and show final stats"""
        print(f"\n{'='*40}")
        print(f"GAME OVER!")
        print(f"Final Stats:")
        print(f"  Name: {self.player.name}")
        print(f"  Health: {self.player.health}/{self.player.max_health}")
        print(f"  XP: {self.player.experience}")
        print(f"{'='*40}")


# ============================================================================
# DEMO: HOE GEBRUIKEN
# ============================================================================

if __name__ == "__main__":
    # Create game
    game = Game()

    # Create player
    game.create_player("Hero", "Warrior", "Village")

    # Start combat
    result = game.start_combat("Goblin", 30, 5, 0)
    print(f"Result: {result}")

    # Show player stats
    print(f"Player health: {game.player.health}/{game.player.max_health}")
    print(f"Player XP: {game.player.experience}")

    # Game end
    game.game_over()
