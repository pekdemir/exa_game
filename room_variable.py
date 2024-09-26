from room import RoomEntity

class RoomVariable(RoomEntity):
    def __init__(self, variable_id, value:int, is_read_only) -> None:
        super().__init__(variable_id)
        self.value = value
        self.is_read_only = is_read_only

    def reset(self) -> None:
        self.value = 0
    
    def read(self) -> int:
        return self.value

    def write(self, data) -> None:
        if not self.is_read_only:
            self.value = data

    def __repr__(self) -> str:
        return f"Variable {self.id}: {self.value} Read Only: {self.is_read_only}"



