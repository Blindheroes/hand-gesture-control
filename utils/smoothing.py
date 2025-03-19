class SmoothingFilter:
    def __init__(self, buffer_size=5):
        self.buffer = []
        self.buffer_size = buffer_size

    def update(self, value):
        self.buffer.append(value)
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
        return sum(self.buffer) / len(self.buffer)
