class Sprite:
    def __init__(self, x, y, bitmap=None, color=None, bg=None):
        # Position
        self.x = x
        self.y = y

        # ANSI color codes
        color_options = {
            "r": "\033[31m",  # Red
            "g": "\033[32m",  # Green
            "y": "\033[33m",  # Yellow
            "b": "\033[34m",  # Blue
            "m": "\033[35m",  # Magenta
            "c": "\033[36m",  # Cyan
            "w": "\033[37m",  # White
            None: ""          # Default
        }
        
        bg_options = {
            "r": "\033[41m",  # Red bg
            "g": "\033[42m",  # Green bg
            "y": "\033[43m",  # Yellow bg
            "b": "\033[44m",  # Blue bg
            "m": "\033[45m",  # Magenta bg
            "c": "\033[46m",  # Cyan bg
            "w": "\033[47m",  # White bg
            None: ""          # Default
        }
        
        # Default bitmap
        if bitmap is None:
            bitmap = [["#", "#"], ["#", "#"]]

        # Apply color and background to every non blank character
        self.bitmap = [
            [
                f"{bg_options.get(bg)}{color_options.get(color)}{char}\033[0m" if char != " " else char
                for char in row
            ]
            for row in bitmap
        ]
    
    # Color functions
    def set_color(self, color):
        color_options = {
            "r": "\033[31m", "g": "\033[32m", "y": "\033[33m",
            "b": "\033[34m", "m": "\033[35m", "c": "\033[36m",
            "w": "\033[37m", None: ""
        }
        for row_idx, row in enumerate(self.bitmap):
            for col_idx, char in enumerate(row):
                char_plain = char.replace("\033[0m", "")
                # Only apply color if it's not a blank space
                if char_plain.strip():
                    self.bitmap[row_idx][col_idx] = f"{color_options.get(color)}{char_plain}\033[0m"

    def set_bg(self, color):
        bg_options = {
            "r": "\033[41m", "g": "\033[42m", "y": "\033[43m",
            "b": "\033[44m", "m": "\033[45m", "c": "\033[46m",
            "w": "\033[47m", None: ""
        }
        for row_idx, row in enumerate(self.bitmap):
            for col_idx, char in enumerate(row):
                char_plain = char.replace("\033[0m", "")
                # Only apply bg if not a blank space
                if char_plain.strip():
                    self.bitmap[row_idx][col_idx] = f"{bg_options.get(color)}{char_plain}\033[0m"

    # Movement functions
    def set_position(self, x, y):
        self.x = x
        self.y = y
