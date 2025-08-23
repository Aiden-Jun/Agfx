import sys
import time
import os

# Terminal functions
def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

class Engine():
    def __init__(self, fps=4):
        # Frame update settings
        self.fps = fps
        self.frame_duration = 1 / fps
        
        # Scene related
        self.current_scene = None
        self.scenes = {}

    def register_scene(self, scene_name, scene):
        # If the scene is a first
        if self.scenes == {}:
            self.current_scene = scene_name
        self.scenes[scene_name] = scene

    def change_current_scene(self, scene_name):
        self.scenes[self.current_scene].stop()
        self.current_scene = scene_name
        self.scenes[self.current_scene].start()

    def render_scene(self):
        self.scenes[self.current_scene].render()

    def run(self):
        # Clear the screen first
        os.system('cls' if os.name == 'nt' else 'clear')
        hide_cursor()

        if self.current_scene is None:
            print("Engine has no scenes")
            return
        
        scene = self.scenes[self.current_scene]
        scene.start()  # Start input thread
        try:
            while scene.running:
                self.render_scene()
                time.sleep(self.frame_duration)
        except KeyboardInterrupt:
            pass
        finally:
            scene.stop()
            show_cursor()
