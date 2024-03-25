class AnimationData:
    def __init__(self, name, duration, frame_rate, objects):
        self.name = name
        self.duration = duration
        self.frame_rate = frame_rate
        self.objects = objects
        self.interpolated_frames = []  # Add this line
