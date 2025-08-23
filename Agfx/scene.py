import readchar
import threading
import time

class Scene():
    def __init__(self, fwidth, fheight, wwidth=None, wheight=None):
        # Frame data
        self.fwidth = fwidth
        self.fheight = fheight
        self.frame = True

        # World setting
        if wwidth == None:
            self.wwidth = fwidth
        else:
            self.wwidth = wwidth

        if wheight == None:
            self.wheight = fheight
        else:
            self.wheight = wheight

        self.wbitmap = [[" "] * self.wwidth for _ in range(self.wheight)]
        self.pixels = [[" "] * self.wwidth for _ in range(self.wheight)]

        # Camera
        self.camera_x = 0
        self.camera_y = 0

        # Sprites
        self.sprites = {}
        self.hidden_sprites = []

        # Key handlers
        self.key_handlers = {}

        # Update handlers
        self.update_handler = None

        # Status
        self.running = False

    # Sprite related functions
    def register_sprite(self, sprite_name, sprite):
        self.sprites[sprite_name] = sprite

    def hide_sprite(self, sprite_name):
        if sprite_name in self.sprites:
            self.hidden_sprites.append(sprite_name)

    def show_sprite(self, sprite_name):
        if sprite_name in self.hidden_sprites:
            self.hidden_sprites.remove(sprite_name)

    def is_sprite_touching(self, sprites_names):
        # Make sure all sprite names exist
        sprites = [self.sprites[name] for name in sprites_names if name in self.sprites]
        if len(sprites) != len(sprites_names):
            return False  # some sprite name not found

        # Get all occupied positions of a sprite as (x, y) tuples
        def sprite_positions(sprite):
            positions = set()
            for row_idx, row in enumerate(sprite.bitmap):
                for col_idx, char in enumerate(row):
                    if char != " ":
                        positions.add((sprite.x + col_idx, sprite.y + row_idx))
            return positions

        # Compute occupied positions for all sprites
        sprite_pos_list = [sprite_positions(s) for s in sprites]

        # Check pairwise adjacency or overlap
        for i in range(len(sprite_pos_list)):
            for j in range(i + 1, len(sprite_pos_list)):
                pos1 = sprite_pos_list[i]
                pos2 = sprite_pos_list[j]

                touching = False
                for x1, y1 in pos1:
                    # Check up/down/left/right neighbors
                    neighbors = [(x1+1, y1), (x1-1, y1), (x1, y1+1), (x1, y1-1)]
                    if pos2 & set(neighbors) or pos2 & pos1:  # Overlapping counts
                        touching = True
                        break
                if not touching:
                    return False

        return True  # All pairs are touching
    
    def is_sprite_touching_frame(self, sprite_name):
        if sprite_name not in self.sprites:
            return (False, [])

        sprite = self.sprites[sprite_name]

        left_wall = 0 if self.frame else -1
        top_wall = 0 if self.frame else -1
        right_wall = self.fwidth - 1 if self.frame else self.fwidth
        bottom_wall = self.fheight - 1 if self.frame else self.fheight

        touching_walls = set()

        for row_idx, row in enumerate(sprite.bitmap):
            for col_idx, char in enumerate(row):
                if char == " ":
                    continue
                px = sprite.x + col_idx
                py = sprite.y + row_idx

                if px <= left_wall:
                    touching_walls.add("l")
                if px >= right_wall:
                    touching_walls.add("r")
                if py <= top_wall:
                    touching_walls.add("t")
                if py >= bottom_wall:
                    touching_walls.add("b")

        if touching_walls:
            return touching_walls
        else:
            return []
    
    # Painting related
    def paint_line(self, char, x, y, dx, dy):
        x0, y0 = x, y
        x1, y1 = dx, dy

        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy  # error value

        while True:
            if 0 <= x0 < self.wwidth and 0 <= y0 < self.wheight:
                self.wbitmap[y0][x0] = char  # paint point
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def register_update_handler(self, handler):
        self.update_handler = handler

    def update_thread(self):
        while self.running:
            self.update_handler()
            time.sleep(0.01)

    def register_key_handler(self, key, handler):
        self.key_handlers[key] = handler

    def input_thread(self):
        while self.running:
            key = readchar.readkey()
            self.key_pressed = key.lower()
            if self.key_pressed in self.key_handlers:
                self.key_handlers[self.key_pressed]()

    def start(self):
        self.running = True
        self._input_thread = threading.Thread(target=self.input_thread, daemon=True)
        self._update_thread = threading.Thread(target=self.update_thread, daemon=True)
        self._input_thread.start()
        self._update_thread.start()

    def stop(self):
        self.running = False

    def toggle_frame(self):
        if self.frame:
            self.frame = False
        else:
            self.frame = True

    def set_camera(self, x, y):
        self.camera_x = x
        self.camera_y = y

    def render(self):
        # Move cursor to top-left
        print("\033[H", end="")

        # Reset pixel buffer
        self.pixels = [[" "] * self.wwidth for _ in range(self.wheight)]

        # First draw the world bitmap
        for y in range(self.wheight):
            for x in range(self.wwidth):
                self.pixels[y][x] = self.wbitmap[y][x]

        # Draw all visible sprites relative to the camera
        for name, sprite in self.sprites.items():
            if name in self.hidden_sprites:
                continue
            for row_idx, row in enumerate(sprite.bitmap):
                for col_idx, char in enumerate(row):
                    # Apply camera offset
                    px = sprite.x - self.camera_x + col_idx
                    py = sprite.y - self.camera_y + row_idx
                    if 0 <= px < self.wwidth and 0 <= py < self.wheight:
                        self.pixels[py][px] = char

        # Build output string
        output_lines = []

        # Top border
        if self.frame:
            output_lines.append("+" + "-" * self.fwidth + "+")

        for row_idx in range(self.fheight):
            line = ""
            for col_idx in range(self.fwidth):
                # Map to camera position in pixel buffer
                buffer_x = col_idx + self.camera_x
                buffer_y = row_idx + self.camera_y
                if 0 <= buffer_x < self.wwidth and 0 <= buffer_y < self.wheight:
                    line += self.pixels[buffer_y][buffer_x]
                else:
                    line += " "
            if self.frame:
                line = "|" + line + "|"
            output_lines.append(line)

        # Bottom border
        if self.frame:
            output_lines.append("+" + "-" * self.fwidth + "+")

        # Print the frame
        print("\n".join(output_lines), end="", flush=True)
