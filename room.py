

class Room:
    def __init__(self, id, row, col) -> None:
        self.id = id
        self.row = row
        self.col = col
        self.slots = [None] * row * col
        self.links = {} # {link_id: room}
    
    def add_slot(self, index, slot) -> None:
        self.slots.insert(index, slot)
    
    def get_slot(self, index):
        return self.slots[index]

    def add_link(self, link_id, room) -> None:
        self.links[link_id] = room

    def get_link(self, link_id):
        return self.links[link_id]
    
    def put_entity(self, entity) -> bool:
        # find first empty slot
        for i, slot in enumerate(self.slots):
            if slot is None:
                self.slots[i] = entity
                entity.room = self
                return True
        return False

    def remove_entity(self, entity) -> bool:
        for i, slot in enumerate(self.slots):
            if slot == entity:
                self.slots[i] = None
                entity.room = None
                return True
        return False
    
    def find_entity(self, type, id):
        for slot in self.slots:
            if slot is not None and isinstance(slot, type) and slot.id == id:
                return slot
        return None
    
    def __repr__(self) -> str:
        return f"Room {self.id}: {self.slots} (Links: {[(key, value.id) for key, value in self.links.items()]})"
    

class RoomEntity:
    def __init__(self, id) -> None:
        self.id = id
        self.room = None
    
    def move(self, link_id) -> bool:
        if link_id in self.room.links:
            curr_room = self.room
            new_room = self.room.links[link_id]
            if(new_room.put_entity(self)):
                curr_room.remove_entity(self)
                self.room = new_room
                return True
        return False

    def __repr__(self) -> str:
        return f"Entity {self.id} as type {type(self)} in Room {self.room.id}"
    