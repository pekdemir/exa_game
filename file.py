import room

class File(room.RoomEntity):
    def __init__(self, file_id) -> None:
        super().__init__(file_id)
        self.name = 'F'
        self.data = []
        self.index = 0
        self.grabbed = False

    def reset(self) -> None:
        self.index = 0

    def is_eof(self) -> bool:
        return self.index == len(self.data)
    
    def is_grabbed(self) -> bool:
        return self.grabbed
    
    def grab(self) -> None:
        self.grabbed = True

    def drop(self) -> None:
        self.grabbed = False

    def read(self):
        if self.index < len(self.data):
            self.index += 1
            return self.data[self.index - 1]
        return None

    def write(self, data) -> None:
        if self.index == len(self.data):
            self.data.append(data)
        else:
            self.data[self.index] = data
        self.index += 1

    def seek(self, offset) -> None:
        new_index = self.index + offset
        if new_index >= len(self.data):
            new_index = len(self.data)
        elif new_index < 0:
            new_index = 0
        self.index = new_index

    def __repr__(self) -> str:
        return f"File {self.id} Data: {self.data} index:({self.index})" + "EOF: " + str(self.is_eof()) 



