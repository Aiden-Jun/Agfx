from Agfx import *

# Create engine
engine = Engine(fps=12)

# Create scene
scene = Scene(50, 20)
engine.register_scene("main scene", scene)

# Create player
player = Sprite(0, 0, color="g")
scene.register_sprite("player", player)

# Movement functions
def move_up():
    walls = scene.is_sprite_touching_frame("player")
    if "t" not in walls:
        player.set_position(player.x, player.y - 1)

def move_down():
    walls = scene.is_sprite_touching_frame("player")
    if "b" not in walls:
        player.set_position(player.x, player.y + 1)

def move_left():
    walls = scene.is_sprite_touching_frame("player")
    if "l" not in walls:
        player.set_position(player.x - 1, player.y)

def move_right():
    walls = scene.is_sprite_touching_frame("player")
    if "r" not in walls:
        player.set_position(player.x + 1, player.y)

# Register key handlers
scene.register_key_handler("w", move_up)
scene.register_key_handler("s", move_down)
scene.register_key_handler("a", move_left)
scene.register_key_handler("d", move_right)

# Run engine
engine.run()