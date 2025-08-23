# Ascii Graphics
Ascii Graphics (Agfx) helps building terminal based apps and games.
## Demo
Simple game where a player can move around inside the frame
```python
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
```
## Terminals

Agfx works on terminals that support ANSI escape codes.
### Supported terminals
- Windows
    - Windows Terminal (modern)
    - ConEmu
    - Cmder
    - Powershell (modern versions)

- Linux / Unix
    - GNOME Terminal
    - Konsole (KDE)
    - Xfce Terminal
    - LXTerminal
    - Tilix
    - Terminator
    - Alacritty
    - Kitty
    - iTerm 2 (macOS)
    - Mac Terminal (built-in)

### Unsupported terminals
- Older Windows
    - cmd.exe
- Lightweight / minimal terminals
    - rxvt / urxvt
    - DOOSBox console
    - Some embedded terminal emulators
- Web based terminals
    - Browser based consoles (Although some could work)
    - Some terminal widgets in editors (Older VS code versions)

## Import

```python
from Agfx import Engine, Scene, Sprite
```
## Sprites
Sprites are like objects in apps or games. They could be a player, text, or anything in ASCII.

### Creation
```python
Sprite(x, y, bitmap, color, bg)
```
- x (int) - X position of the sprite
- y (int) - Y position of the sprite
- bitmap (optional) - The ASCII look of the sprite, can be created using bitmapper.py
- color & bg (string) (optional) - Color and background of the sprite
    - r - Red
    - g - Green
    - y - Yellow
    - b - Blue
    - m - Magenta
    - c - Cyan
    - w - White

### Accessible / Changeable Variables
- bitmap - Change the look of a sprite
- x - X position of the sprite
- y - Y position of the sprite

### Functions

#### Looks
Change color
```python
set_color(color)
```

Change background
```python
set_bg(color)
```

#### Movement
Set position
```python
set_position(x, y)
```
## Scene

### Creation
```python
Scene(fwidth, fheight, wwidth, wheight)
```
- fwidth (int) - Frame width
- fheight (int) - Frame height
- wwidth (int) (optional) - World width
- wheight (int) (optional) - World height

### Accessible / Changeable Variables
- fwidth - Frame width
- fheight - Frame height
- camera_x - Camera x value
- camera_y - Camera y value

### Functions

#### Sprite
Add sprite
```python
register_sprite(sprite_name, sprite)
```
Hide sprite
```python
hide_sprite(sprite_name)
```
Show sprite
```python
show_sprite(sprite_name)
```
Sprite touching - takes in a list of sprite names and returns true if all are touching
```python
is_sprite_touching(sprite_names)
```

#### Painting
Paint a line
```python
paint_line(char, x, y, dx, dy)
```

Sprite touching frame - takes sprite name and gives a list of walls
- t - top
- b - bottom
- l - left
- r - right

```python
is_sprite_touching_frame(sprite_name)
```

#### Key handling

Add key handler function - after adding, the function will run when that key is pressed
```python
register_key_handler(key, handler)
```

#### Update handling

Add a function that keeps running while the scene is being played
```python
register_update_handler(handler)
```

#### Looks
Toggle frame around the scene (on by default)
```python
toggle_frame()
```

## Engine

### Creation
```python
Engine(fps)
```

- fps - Frames per second, how often the frame updates, default 4

### Functions

#### Scene
Add scene
```python
register_scene(scene_name, scene)
```

Change the currrent scene
```python
change_current_scene(scene_name)
```

Run the engine
```python
run()
```