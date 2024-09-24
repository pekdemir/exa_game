from room import RoomEntity

class RoomVariable(RoomEntity):
    def __init__(self, variable_id, is_read_only) -> None:
        super().__init__(variable_id)
        self.data = 0
        self.is_read_only = is_read_only

    def reset(self) -> None:
        self.index = 0
    
    def read(self):
        return self.data

    def write(self, data) -> None:
        if not self.is_read_only:
            self.data = data

    def __repr__(self) -> str:
        return f"Variable {self.id}: {self.data} Read Only: {self.is_read_only}" 



