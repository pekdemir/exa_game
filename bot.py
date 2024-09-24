from room import RoomEntity
from file import File

class Instruction:
    def __init__(self) -> None:
        self.opcode = None
        self.args = []

    def __init__(self, instruction_str) -> None:
        parts = instruction_str.split(" ")
        # print(parts)
        self.opcode = parts[0]
        self.args = parts[1:]

class Register:
    def __init__(self, name) -> None:
        self.name = name
        self.value = 0
    
    def read(self) -> int:
        return self.value
    
    def write(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return str(self.value)

class Bot(RoomEntity):
    def __init__(self, bot_id) -> None:
        super().__init__(bot_id)
        self.instructions = []
        self.labels = {}
        self.regs = {'X': Register('X'), 'T': Register('T'), 'F': None, 'M': None, 'PC': 0}
        self.isLocal = False
        self.alive = True
        print(f"Bot {self.id} created")
        
    def print_state(self) -> None:
        print("Registers:")
        print(f"\tX: {self.regs['X']}")
        print(f"\tT: {self.regs['T']}")
        print(f"\tF: {self.regs['F']}")
        print(f"\tM: {self.regs['M']}")
        print(f"\tPC: {self.regs['PC']}")
        print("Labels:")
        for label in self.labels:
            print(f"\t{label}: {self.labels[label]}")
        print("Instructions:")
        for i,instruction in enumerate(self.instructions):
            if i == self.regs["PC"]:
                print(f"\t> {instruction.opcode} {' '.join(instruction.args)}")
            else:
                print(f"\t{instruction.opcode} {' '.join(instruction.args)}")

    def parse_code_from_file(self, file_name) -> None:
        with open(file_name, 'r') as file:
            code_str = file.read()
            self.parse_code(code_str)  

    def parse_code(self, code_str) -> None:
        self.code = code_str
        lines = self.code.split("\n")
        index = 0
        for line in lines:
            instruction = Instruction(line)
            self.instructions.append(instruction)
            if instruction.opcode == "MARK":
                self.labels[instruction.args[0]] = index
            index += 1
        self.print_state()
    
    def _get_value(self, arg) -> int:
        if arg == 'X' or arg == 'T' or arg == 'F' or arg == 'M':
            return self.regs[arg].read()
        else:
            return int(arg)
    
    def _get_reg(self, arg) -> str:
        if arg != 'X' and arg != 'T' and arg != 'F' and arg != 'M':
            raise Exception("Argument must be X,T,F or M register")
        else:
            return self.regs[arg].name
        
    def _arg_check(self, instruction, num_args) -> None:
        if len(instruction.args) != num_args:
            raise Exception(f"{instruction.opcode} requires {num_args} arguments")

    def _step(self) -> bool:
        if self.regs["PC"] >= len(self.instructions):
            return False
        instruction = self.instructions[self.regs["PC"]]

        match instruction.opcode:
            case "JUMP":
                self._arg_check(instruction, 1)
                if not instruction.args[0] in self.labels:
                    raise Exception(f"Label {instruction.args[0]} not found")
                self.regs["PC"] = self.labels[instruction.args[0]]

            case "LINK":
                self._arg_check(instruction, 1)
                link_id = instruction.args[0]
                if not self.move(link_id):
                    raise Exception(f"Link {link_id} not found")
                if self.regs['F'] is not None:
                    if not self.regs['F'].move(link_id):
                        raise Exception(f"Link {link_id} not found")

            case "COPY":
                self._arg_check(instruction, 2)
                dest = self._get_reg(instruction.args[1])
                source = self._get_value(instruction.args[0])
                self.regs[dest].write(source)

            case "ADDI":
                self._arg_check(instruction, 3)
                dest = self._get_reg(instruction.args[2])
                first = self._get_value(instruction.args[0])
                second = self._get_value(instruction.args[1])
                self.regs[dest].write(first + second)

            case "SUBI":
                self._arg_check(instruction, 3)
                dest = self._get_reg(instruction.args[2])
                first = self._get_value(instruction.args[0])
                second = self._get_value(instruction.args[1])
                self.regs[dest].write(first - second)

            case "MULI":
                self._arg_check(instruction, 3)
                dest = self._get_reg(instruction.args[2])
                first = self._get_value(instruction.args[0])
                second = self._get_value(instruction.args[1])
                self.regs[dest].write(first * second)

            case "DIVI":
                self._arg_check(instruction, 3)
                dest = self._get_reg(instruction.args[2])
                first = self._get_value(instruction.args[0])
                second = self._get_value(instruction.args[1])
                self.regs[dest].write(first // second)

            case "GRAB":
                self._arg_check(instruction, 1)
                file_id = self._get_value(instruction.args[0])
                file = self.room.find_entity(File, file_id)
                if file is None:
                    raise Exception(f"File {file_id} not found")
                if file.is_grabbed():
                    raise Exception(f"File {file_id} already grabbed")
                file.reset()
                file.grab()
                self.regs["F"] = file
                
            case "DROP":
                if self.regs["F"] is None:
                    raise Exception("No file grabbed")
                self.regs["F"].drop()
                self.regs["F"] = None

            case "SEEK":
                self._arg_check(instruction, 1)
                if self.regs["F"] is None:
                    raise Exception("No file grabbed")
                index = self._get_value(instruction.args[0])
                self.regs["F"].seek(index)

            case "HALT":
                return False
            
            case "KILL":
                pass

            case "REPL":
                self._arg_check(instruction, 1)
                pass

            case "TEST":
                if len(instruction.args) == 1:
                    if instruction.args[0] == "EOF":
                        if self.regs["F"] is None:
                            raise Exception("No file grabbed")
                        self.regs["T"] = 1 if self.regs["F"].is_eof() else 0
                    else:
                        raise Exception("Invalid argument")
                else:
                    self._arg_check(instruction, 3)
                    first = self._get_reg(instruction.args[0])
                    second = self._get_value(instruction.args[2])
                    operator = instruction.args[1]
                    if operator == "==":
                        self.regs["T"] = 1 if self.regs[first].read() == second else 0
                    elif operator == "!=":
                        self.regs["T"] = 1 if self.regs[first].read() != second else 0
                    elif operator == "<":
                        self.regs["T"] = 1 if self.regs[first].read() < second else 0
                    elif operator == ">":
                        self.regs["T"] = 1 if self.regs[first].read() > second else 0
                    elif operator == "<=":
                        self.regs["T"] = 1 if self.regs[first].read() <= second else 0
                    elif operator == ">=":
                        self.regs["T"] = 1 if self.regs[first].read() >= second else 0
                    else:
                        raise Exception("Invalid operator")
                    
            case "FJMP":
                self._arg_check(instruction, 1)
                if self.regs["T"] == 0:
                    if not instruction.args[0] in self.labels:
                        raise Exception(f"Label {instruction.args[0]} not found")
                    self.regs["PC"] = self.labels[instruction.args[0]]

            case "TJMP":
                self._arg_check(instruction, 1)
                if self.regs["T"] != 0:
                    if not instruction.args[0] in self.labels:
                        raise Exception(f"Label {instruction.args[0]} not found")
                    self.regs["PC"] = self.labels[instruction.args[0]]

            case "MAKE":
                pass

            case "MARK":
                pass
            
            case _:
                raise Exception(f"Unknown instruction {instruction.opcode}")

        self.regs["PC"] += 1
        return True


    def destroy(self) -> None:
        self.room.remove_entity(self)
        self.alive = False
        print(f"Bot {self.id} destroyed")

    def step(self) -> bool:
        result = self._step()
        # self.print_state()
        return result
    
    def run(self) -> None:
        try:
            while self._step():
                self.print_state()
        except Exception as e:
            print(e)
            self.destroy()
        
    def __repr__(self) -> str:
        return f"Bot {self.id} alive: {self.alive}"
            