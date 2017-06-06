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
    PLAYER_COUNT = 4

    MAP_WIDTH = 800
    MAP_HEIGHT = 600

    ENEMY_SPAWN_DELAY = 1
    ENEMY_LIMIT = 5

    # Player
    P_SPEED = 20
    P_RANGE_VISIBLE = 100
    P_RANGE_ATTACKABLE = 20
    P_AMMO = 10
    P_DAMAGE = 100
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

    # Enemy
    ENEMY_SPEED = 30

    # Entity
    E_POS = Vector(0,0)
    E_VEL = Vector(0,0)
    E_SPEED = 10
    E_SIZE = 10
    E_HEALTHMAX = 100
