from room import Room, RoomEntity
from floor import Floor
from bot import Bot
from file import File
from room_variable import RoomVariable
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

    bot1 = Bot("bot1")
    bot1.parse_code_from_file("prog1.exa")
    room1.put_entity(bot1)
    # bot.run()

    bot2 = Bot("bot2")
    bot2.parse_code_from_file("prog2.exa")
    room1.put_entity(bot2)
    # bot.run()

    scheduler = Scheduler()
    scheduler.add_bot(bot1)
    scheduler.add_bot(bot2)
    
    cmd = input(">")
    while cmd != "exit":
        cmd = cmd.split(" ")
        if cmd[0] == "step":
            scheduler.cycle()
        elif cmd[0] == "room":
            room = floor.find_entity(Room, cmd[1])
            if room is not None:
                print(room)
            else:
                print("Room not found")
        elif cmd[0] == "floor":
            floor.print_floor()
        elif cmd[0] == "bot":
            bot = floor.find_entity(Bot, cmd[1])
            if bot is not None:
                bot.print_state()
            else:
                print("Bot not found")
        elif cmd[0] == "file":
            file = floor.find_entity(File, cmd[1])
            if file is not None:
                print(file)
            else:
                print("File not found")
        elif cmd[0] == "variable":
            variable = floor.find_entity(RoomVariable, cmd[1])
            if variable is not None:
                print(variable)
            else:
                print("Variable not found")

        cmd = input(">")

    # while scheduler.cycle():
    #     pass


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