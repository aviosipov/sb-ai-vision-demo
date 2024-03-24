import json
from editor.animation_data import AnimationData

class AnimationDataManager:
    def __init__(self):
        self.animation_data = None

    def load_animation_data(self):
        try:
            with open("animation_data.json", "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.animation_data = AnimationData(data.get("name", ""), data.get("duration", 0.0), data.get("frame_rate", 0), data.get("objects", []))
                else:
                    print("Invalid animation data format. Using default values.")
                    self.animation_data = self.create_default_animation_data()
        except FileNotFoundError:
            print("Animation data file not found. Using default values.")
            self.animation_data = self.create_default_animation_data()

    def save_animation_data(self):
        data = {
            "name": self.animation_data.name,
            "duration": self.animation_data.duration,
            "frame_rate": self.animation_data.frame_rate,
            "objects": self.animation_data.objects
        }
        with open("animation_data.json", "w") as file:
            json.dump(data, file)

    def update_animation_data(self, animation_data):
        self.animation_data = animation_data

    def create_default_animation_data(self):
        objects = [
            {"name": "Player", "imagePath": "player.png", "keyframes": []},
            {"name": "Enemy", "imagePath": "enemy.png", "keyframes": []}
        ]
        return AnimationData("DefaultAnimation", 2.0, 60, objects)