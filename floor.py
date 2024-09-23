from room import Room
import json

class Floor:
    def __init__(self) -> None:
        self.rooms = {}
    
    def parse_from_json_file(self, file_path) -> None:
        with open(file_path) as file:
            json_context = json.load(file)
            for room_data in json_context["Rooms"]:
                room = Room(room_data["id"], room_data["row"], room_data["col"])
                self.add_room(room)
            for room_data in json_context["Rooms"]:
                room = self.get_room(room_data["id"])
                for link_id, link_room_id in room_data["Links"].items():
                    room.add_link(link_id, self.get_room(link_room_id))
            
    def print_floor(self) -> None:
        for room in self.rooms.values():
            print(f"Room {room.id}")
            for link_id, link_room in room.links.items():
                print(f"Link {link_id} to Room {link_room.id}")

    def add_room(self, room) -> None:
        self.rooms[room.id] = room
    
    def get_room(self, room_id) -> Room:
        return self.rooms[room_id]
    