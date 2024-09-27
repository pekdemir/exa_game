import room
import bot
import file
import room_variable
import globals
import json

class CmdDebug:
    def __init__(self):
        pass

    def run(self):
        cmd = input("> ")
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
                            new_room = room.Room(cmd[2], int(cmd[3]), int(cmd[4]))
                            globals.game_globals.floor.add_room(new_room)
                        case "bot":
                            which_room = globals.game_globals.floor.find_entity(room.Room, cmd[3])
                            new_bot = bot.Bot(cmd[2])
                            which_room.put_entity(new_bot)
                            globals.game_globals.scheduler.add_bot(new_bot)
                        case "file":
                            which_room = globals.game_globals.floor.find_entity(room.Room, cmd[3])
                            new_file = file.File(cmd[2])
                            which_room.put_entity(new_file)
                        case "variable":
                            which_room = globals.game_globals.floor.find_entity(room.Room, cmd[5])
                            variable = room_variable.RoomVariable(cmd[2], int(cmd[3]), True if cmd[4] == "true" else False)
                            which_room.put_entity(variable)
                        case "link":
                            room1 = globals.game_globals.floor.find_entity(room.Room, cmd[2])
                            room2 = globals.game_globals.floor.find_entity(room.Room, cmd[3])
                            link_id = cmd[4]
                            room1.add_link(link_id, room2)
                        case _:
                            print("Invalid entity type")
                case "code":
                    if globals.game_globals.scheduler.first_start == False:
                        print("Code can only be entered before the scheduler is run")
                    else:
                        which_bot = globals.game_globals.floor.find_entity(bot.Bot, cmd[1])
                        print(f"Enter code for bot {cmd[1]}, enter <return> to finish:")
                        code = ""
                        code_line = input("-")
                        while code_line != "":
                            code += code_line + "\n"
                            code_line = input("-")
                        which_bot.parse_code(code)
                case "step":
                    globals.game_globals.scheduler.cycle()
                case "run":
                    if len(cmd) > 1:
                        count = int(cmd[1])
                        for i in range(count):
                            globals.game_globals.scheduler.cycle()
                    else:
                        while globals.game_globals.scheduler.cycle():
                            pass
                case "room":
                    which_room = globals.game_globals.floor.find_entity(room.Room, cmd[1])
                    if which_room is not None:
                        print(which_room)
                    else:
                        print("Room not found")
                case "floor":
                    globals.game_globals.floor.print_floor()
                case "bot":
                    which_bot = globals.game_globals.floor.find_entity(bot.Bot, cmd[1])
                    if which_bot is not None:
                        which_bot.print_state()
                    else:
                        print("Bot not found")
                case "file":
                    which_file = globals.game_globals.floor.find_entity(file.File, int(cmd[1]))
                    if which_file is not None:
                        print(which_file)
                    else:
                        print("File not found")
                case "variable":
                    variable = globals.game_globals.floor.find_entity(room_variable.RoomVariable, cmd[1])
                    if variable is not None:
                        print(variable)
                    else:
                        print("Variable not found")
                case "load":
                    with open(cmd[1], 'r') as json_file:
                        json_context = json.load(json_file)
                        for room_data in json_context["Rooms"]:
                            new_room = room.Room(room_data["id"], int(room_data["row"]), int(room_data["col"]))
                            globals.game_globals.floor.add_room(new_room)
                        for link_data in json_context["Links"]:
                            from_room = globals.game_globals.floor.get_room(link_data["from"])
                            to_room = globals.game_globals.floor.get_room(link_data["to"])
                            from_room.add_link(link_data["id"], to_room)
                        for bot_data in json_context["Bots"]:
                            which_room = globals.game_globals.floor.get_room(bot_data["room"])
                            new_bot = bot.Bot(bot_data["id"])
                            which_room.put_entity(new_bot)
                            globals.game_globals.scheduler.add_bot(new_bot)
                        for file_data in json_context["Files"]:
                            which_room = globals.game_globals.floor.get_room(file_data["room"])
                            new_file = file.File(int(file_data["id"]))
                            for data_val in file_data["data"]:
                                new_file.write(int(data_val))
                            new_file.reset()
                            which_room.put_entity(new_file)
                        for variable_data in json_context["Variables"]:
                            which_room = globals.game_globals.floor.get_room(variable_data["room"])
                            variable = room_variable.RoomVariable(variable_data["id"], int(variable_data["value"]), variable_data["read_only"])
                            which_room.put_entity(variable)

                case _:
                    print("Invalid command")
            cmd = input("> ")