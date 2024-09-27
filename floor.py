import room
import json

class Floor:
    def __init__(self) -> None:
        self.rooms = {}
    
    def parse_from_json_file(self, file_path) -> None:
        with open(file_path) as file:
            json_context = json.load(file)
            for room_data in json_context["Rooms"]:
                new_room = room.Room(room_data["id"], room_data["row"], room_data["col"])
                self.add_room(new_room)
            for room_data in json_context["Rooms"]:
                which_room = self.get_room(room_data["id"])
                for link_id, link_room_id in room_data["Links"].items():
                    which_room.add_link(link_id, self.get_room(link_room_id))
            
    def print_floor(self) -> None:
        for a_room in self.rooms.values():
            print(f"Room {a_room.id}")
            for link_id, link_room in a_room.links.items():
                print(f"Link {link_id} to Room {link_room.id}")

    def add_room(self, a_room) -> None:
        self.rooms[a_room.id] = a_room
    
    def get_room(self, room_id) -> room.Room:
        return self.rooms[room_id]
    
    def find_entity(self, type, id):
        if type == room.Room and id in self.rooms:
            return self.get_room(id)
        for a_room in self.rooms.values():
            entity = a_room.find_entity(type, id)
            if entity is not None:
                return entity
        return None
    