from room import Room, RoomEntity
from floor import Floor
from bot import Bot
from file import File
from room_variable import RoomVariable
from scheduler import Scheduler 


class CmdDebug:
    def __init__(self):
        self.floor = Floor()
        self.scheduler = Scheduler()
    
    def run(self):
        cmd = input(">")
        while cmd != "exit":
            cmd = cmd.split(" ")
            match cmd[0]:
                case "help":
                    print("Commands:")
                    print("help - print this help message")
                    print("add - add an entity to the floor")
                    print("    room <room_id> <row> <col> - add a room to the floor")
                    print("    bot <bot_id> <room_id> - add a bot to the room")
                    print("    file <file_id> <room_id> - add a file to the room")
                    print("    variable <variable_id> <data> <is_persistent> <room_id>- add a variable to the room")
                    print("    link <room_id1> <room_id2> <link_id> - add a link between rooms")
                    print("run <count> - run the scheduler for <count> cycles")
                    print("step - run one step of the scheduler")
                    print("room <room_id> - print room details")
                    print("floor - print floor details")
                    print("bot <bot_id> - print bot details")
                    print("file <file_id> - print file details")
                    print("variable <variable_id> - print variable details")
                    print("exit - exit the program")

                case "add":
                    match cmd[1]:
                        case "room":
                            room = Room(cmd[2], int(cmd[3]), int(cmd[4]))
                            self.floor.add_room(room)
                        case "bot":
                            room = self.floor.find_entity(Room, cmd[3])
                            bot = Bot(cmd[2])
                            room.put_entity(bot)
                            self.scheduler.add_bot(bot)
                        case "file":
                            room = self.floor.find_entity(Room, cmd[3])
                            file = File(cmd[2])
                            room.put_entity(file)
                        case "variable":
                            room = self.floor.find_entity(Room, cmd[5])
                            variable = RoomVariable(cmd[2], int(cmd[3]), True if cmd[4] == "true" else False)
                            room.put_entity(variable)
                        case "link":
                            room1 = self.floor.find_entity(Room, cmd[2])
                            room2 = self.floor.find_entity(Room, cmd[3])
                            link_id = cmd[4]
                            room1.add_link(link_id, room2)
                        case _:
                            print("Invalid entity type")
                case "code":
                    if self.scheduler.first_start == False:
                        print("Code can only be entered before the scheduler is run")
                        break
                    bot = self.floor.find_entity(Bot, cmd[1])
                    print(f"Enter code for bot {cmd[1]}, enter <return> to finish:")
                    code = ""
                    code_line = input("-")
                    while code_line != "":
                        code += code_line + "\n"
                        code_line = input("-")
                    bot.parse_code(code)
                case "step":
                    self.scheduler.cycle()
                case "run":
                    if len(cmd) > 1:
                        count = int(cmd[1])
                        for i in range(count):
                            self.scheduler.cycle()
                    else:
                        while self.scheduler.cycle():
                            pass
                case "room":
                    room = self.floor.find_entity(Room, cmd[1])
                    if room is not None:
                        print(room)
                    else:
                        print("Room not found")
                case "floor":
                    self.floor.print_floor()
                case "bot":
                    bot = self.floor.find_entity(Bot, cmd[1])
                    if bot is not None:
                        bot.print_state()
                    else:
                        print("Bot not found")
                case "file":
                    file = self.floor.find_entity(File, int(cmd[1]))
                    if file is not None:
                        print(file)
                    else:
                        print("File not found")
                case "variable":
                    variable = self.floor.find_entity(RoomVariable, cmd[1])
                    if variable is not None:
                        print(variable)
                    else:
                        print("Variable not found")
                case _:
                    print("Invalid command")
            cmd = input(">")