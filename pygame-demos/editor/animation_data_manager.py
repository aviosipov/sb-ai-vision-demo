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
        self.generate_interpolated_frames()  # Add this line

    def create_default_animation_data(self):
        objects = [
            {"name": "Player", "imagePath": "player.png", "keyframes": []},
            {"name": "Enemy", "imagePath": "enemy.png", "keyframes": []}
        ]
        return AnimationData("DefaultAnimation", 2.0, 60, objects)
    

    def generate_interpolated_frames(self):
        self.animation_data.interpolated_frames = []  # Clear existing interpolated frames
        for obj_index, obj in enumerate(self.animation_data.objects):
            keyframes = obj["keyframes"]
            if len(keyframes) > 1:
                for i in range(len(keyframes) - 1):
                    start_frame = keyframes[i]["frameNumber"]
                    end_frame = keyframes[i + 1]["frameNumber"]
                    start_pos = keyframes[i]["position"]
                    end_pos = keyframes[i + 1]["position"]

                    for frame in range(start_frame + 1, end_frame):
                        t = (frame - start_frame) / (end_frame - start_frame)
                        interpolated_pos = [
                            start_pos[0] + t * (end_pos[0] - start_pos[0]),
                            start_pos[1] + t * (end_pos[1] - start_pos[1])
                        ]
                        interpolated_frame = {
                            "frameNumber": frame,
                            "objectIndex": obj_index,  # Add this line
                            "position": interpolated_pos,
                            "scale": [1, 1],
                            "rotation": 0,
                            "opacity": 1.0
                        }
                        self.animation_data.interpolated_frames.append(interpolated_frame)