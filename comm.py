class Comm():
    def __init__(self):
        self.name = 'M'
        self.data = 0

    def read(self):
        return self.data

    def write(self, data):
        self.data = data

    def __eq__(self, value: object) -> bool:
        self.write(value)


