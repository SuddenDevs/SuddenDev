from .vector import Vector

class GameConfig:
    # Game steps per second
    # simulation rate >= display rate
    FRAMERATE_SIM = 30
    FRAMERATE_DISPLAY = 30
    FRAME_INTERVAL_SIM = 1/FRAMERATE_SIM
    FRAME_INTERVAL_DISPLAY = 1/FRAMERATE_DISPLAY

    # Packet size in number of game states
    BATCHSIZE = 500

    # Game
    TIME_LIMIT = 15

    MAP_WIDTH = 800
    MAP_HEIGHT = 600

    # Enemy
    ENEMY_ATTACK_DELAY = 30

    BASE_ENEMY_SPEED = 30
    BASE_ENEMY_SPAWN_DELAY = 1
    BASE_ENEMY_LIMIT = 3
    BASE_ENEMY_RANGE_ATTACKABLE = 15
    BASE_ENEMY_DAMAGE = 10

    # Probability of an enemy spawning on each frame, if the enemy limit has
    # not been reached. The expected number of frames between enemy spawn is
    # given by 1/ENEMY_SPAWN_PROBABILITY, given by the Binomial distribution.
    BASE_ENEMY_SPAWN_PROBABILITY = 0.1

    # Difficulty scaling
    # Increased by x = x + wave_number * scale
    ENEMY_SPEED_SCALE = 1
    ENEMY_DAMAGE_SCALE = 2
    ENEMY_RANGE_ATTACKABLE_SCALE = 1
    ENEMY_SPAWN_DELAY_SCALE = 0
    ENEMY_LIMIT_SCALE = 3
    ENEMY_SPAWN_PROBABILITY_SCALE = 0.1

    # Player
    P_SPEED = 80
    P_RANGE_VISIBLE = 400
    P_RANGE_ATTACKABLE = 20
    P_AMMO = 6
    P_DAMAGE = 80
    P_ATTACK_DELAY = 10
    P_DEFAULT_SCRIPT = """
timer = 0

def update(player, delta):
    global timer
    timer += delta

    # Find Target
    min_dist = sys.float_info.max
    target = None
    for e in enemies_visible:
        mag = Vector.Length(e.pos - player.pos)
        if mag < min_dist:
            min_dist = mag
            target = e

    if target is not None:
        diff = player.pos - target.pos
        mag = min(player.speed, min_dist)
        player.vel = Vector.Normalize(diff) * mag
    else:
        player.vel = Vector(0,0)
    """

    # Entity
    E_POS = Vector(0,0)
    E_VEL = Vector(0,0)
    E_SPEED = 10
    E_SIZE = 10
    E_HEALTHMAX = 100

    # Powerups
    POW_SIZE = 50
    POW_AMMO_UP_VALUE = 10
    POW_HEALTH_UP_VALUE = 50 

    # Limit of powerups spawned per wave
    POW_LIMIT = 15
    POW_SPAWN_DELAY = 3
    POW_SPAWN_PROBABILITY = 0.02

    def __init__(self, wave):
        if wave <= 0:
            wave = 1
        
        scale = wave - 1

        # Enemy
        self.ENEMY_SPEED = self.BASE_ENEMY_SPEED + scale * self.ENEMY_SPEED_SCALE
        self.ENEMY_RANGE_ATTACKABLE = self.BASE_ENEMY_RANGE_ATTACKABLE + scale * self.ENEMY_RANGE_ATTACKABLE_SCALE
        self.ENEMY_DAMAGE = self.BASE_ENEMY_DAMAGE + scale * self.ENEMY_DAMAGE_SCALE
        self.ENEMY_SPAWN_DELAY = self.BASE_ENEMY_SPAWN_DELAY + scale * self.ENEMY_SPAWN_DELAY_SCALE
        self.ENEMY_LIMIT = self.BASE_ENEMY_LIMIT + scale * self.ENEMY_LIMIT_SCALE
        self.ENEMY_SPAWN_PROBABILITY = self.BASE_ENEMY_SPAWN_PROBABILITY + scale * self.ENEMY_SPAWN_PROBABILITY_SCALE

        # Cap probability at 1
        if self.ENEMY_SPAWN_PROBABILITY >= 1:
            self.ENEMY_SPAWN_PROBABILITY = 1
