from .vector import Vector

class GameConfig:
    # Game steps per second
    # simulation rate >= display rate
    FRAMERATE_SIM = 30
    FRAMERATE_DISPLAY = 30
    FRAME_INTERVAL_SIM = 1/FRAMERATE_SIM
    FRAME_INTERVAL_DISPLAY = 1/FRAMERATE_DISPLAY

    # Timeout in seconds before the user script is rejected
    SCRIPT_TIMEOUT = 3

    # Packet size in number of game states
    BATCHSIZE = 500

    # Game
    TIME_LIMIT = 300

    MAP_WIDTH = 800
    MAP_HEIGHT = 600

    # Core
    CORE_HEALTH = 400

    # Enemy
    ENEMY_ATTACK_DELAY = 30

    BASE_ENEMY_SPEED = 30
    BASE_ENEMY_SPAWN_DELAY = 1
    BASE_ENEMY_LIMIT = 10
    BASE_ENEMY_RANGE_VISIBLE = 200
    BASE_ENEMY_RANGE_ATTACKABLE = 30
    BASE_ENEMY_DAMAGE = 10
    BASE_ENEMY_HEALTH = 100

    # Probability of an enemy spawning on each frame, if the enemy limit has
    # not been reached. The expected number of frames between enemy spawn is
    # given by 1/ENEMY_SPAWN_PROBABILITY, given by the Binomial distribution.
    BASE_ENEMY_SPAWN_PROBABILITY = 0.1

    # Difficulty scaling
    # Increased by x = x + wave_number * scale
    ENEMY_HEALTH_SCALE = 20
    ENEMY_SPEED_SCALE = 1
    ENEMY_DAMAGE_SCALE = 2
    ENEMY_RANGE_ATTACKABLE_SCALE = 1
    ENEMY_RANGE_VISIBLE_SCALE = 10
    ENEMY_SPAWN_DELAY_SCALE = 0
    ENEMY_LIMIT_SCALE = 2
    ENEMY_SPAWN_PROBABILITY_SCALE = 0.1

    BOSS_SIZE_SCALE = 3
    BOSS_HEALTH_SCALE = 10
    BOSS_DAMAGE_SCALE = 10
    BOSS_STATS_SCALE = 10
    BOSS_WAVE_MULTIPLES = 5

    # Player
    P_SPEED = 80
    P_RANGE_VISIBLE = 300
    P_RANGE_ATTACKABLE = 80
    P_AMMO = 10
    P_DAMAGE = 75
    P_ATTACK_DELAY = 10
    P_DEFAULT_SCRIPT = """
# Default script
# Check the documentation to read more about how to script your bot!

def update(player, delta):
    # Find the nearest enemy, move towards it and shoot it
    nearest_enemy = get_nearest_enemy()
    move_to(nearest_enemy)
    shoot(nearest_enemy)
"""

    # Entity
    E_POS = Vector(0,0)
    E_VEL = Vector(0,0)
    E_SPEED = 10
    E_SIZE = 10
    E_HEALTHMAX = 100

    # Powerups
    POW_SIZE = 14
    POW_AMMO_UP_VALUE = 10
    POW_HEALTH_UP_VALUE = 50 

    # Limit of powerups spawned per wave
    POW_LIMIT = 15
    POW_SPAWN_DELAY = 3
    POW_SPAWN_PROBABILITY = 0.02

    def __init__(self, wave):
        if wave <= 0:
            wave = 1
        
        if wave % self.BOSS_WAVE_MULTIPLES == 0:
            boss_level = wave / self.BOSS_WAVE_MULTIPLES
            boss_scale = boss_level * self.BOSS_STATS_SCALE

            scale = boss_scale
            self.ENEMY_LIMIT = boss_level
            self.ENEMY_SIZE = self.E_SIZE * boss_level * self.BOSS_SIZE_SCALE
            self.ENEMY_HEALTH = boss_level * self.BOSS_HEALTH_SCALE * self.BASE_ENEMY_HEALTH
        else:
            # Enemy
            scale = wave - 1
            self.ENEMY_LIMIT = self.BASE_ENEMY_LIMIT + scale * self.ENEMY_LIMIT_SCALE
            self.ENEMY_SIZE = self.E_SIZE
            self.ENEMY_HEALTH = self.BASE_ENEMY_HEALTH + scale * self.ENEMY_HEALTH_SCALE

        self.ENEMY_RANGE_VISIBLE = self.BASE_ENEMY_RANGE_VISIBLE + scale * self.ENEMY_RANGE_VISIBLE_SCALE + self.ENEMY_SIZE
        self.ENEMY_SPEED = self.BASE_ENEMY_SPEED + scale * self.ENEMY_SPEED_SCALE
        self.ENEMY_RANGE_ATTACKABLE = self.BASE_ENEMY_RANGE_ATTACKABLE + scale * self.ENEMY_RANGE_ATTACKABLE_SCALE + self.ENEMY_SIZE
        self.ENEMY_DAMAGE = self.BASE_ENEMY_DAMAGE + scale * self.ENEMY_DAMAGE_SCALE
        self.ENEMY_SPAWN_DELAY = self.BASE_ENEMY_SPAWN_DELAY + scale * self.ENEMY_SPAWN_DELAY_SCALE
        self.ENEMY_SPAWN_PROBABILITY = self.BASE_ENEMY_SPAWN_PROBABILITY + scale * self.ENEMY_SPAWN_PROBABILITY_SCALE

        # Cap probability at 1
        if self.ENEMY_SPAWN_PROBABILITY >= 1:
            self.ENEMY_SPAWN_PROBABILITY = 1
