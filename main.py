from room import Room, RoomEntity
from floor import Floor
from bot import Bot
from file import File
from scheduler import Scheduler 

class DummyEntity(RoomEntity):
    def __init__(self) -> None:
        super().__init__()




if __name__=="__main__":
    floor = Floor()

    floor.parse_from_json_file("floor_config.json")
    floor.print_floor()

    room1 = floor.get_room("room1")

    file = File(199)
    room1.put_entity(file)

    bot1 = Bot("bot1", "prog1.exa")
    room1.put_entity(bot1)
    # bot.run()

    bot2 = Bot("bot2", "prog2.exa")
    room1.put_entity(bot2)
    # bot.run()

    scheduler = Scheduler()
    scheduler.add_bot(bot1)
    scheduler.add_bot(bot2)
    
    while scheduler.cycle():
        pass
    # room1 = Room("room1", 3)
    # room2 = Room("room2", 3)

    # room1.add_link(800, room2)
    # room2.add_link(-1, room1)

    # floor.add_room(room1)
    # floor.add_room(room2)

    # dummy = DummyEntity()
    # dummy2 = DummyEntity()
    # room1.put_entity(dummy)
    # room1.put_entity(dummy2)
    # print(room1.slots)
    # print(room2.slots)
    # print(dummy.room.id)
    # print(dummy.move(800))
    # print(dummy.move(-1))
    # print(dummy.room.id)
    # print(room1.slots)
    # print(room2.slots)