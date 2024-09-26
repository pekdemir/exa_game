from enum import IntEnum

class Communication:
    def __init__(self):
        self.provider_list = []

    def add_sender(self, sender, data) -> None:
        self.provider_list.append({'sender': sender, 'data': data})
    
    def remove_sender(self, sender) -> None:
        self.provider_list = [x for x in self.provider_list if x['sender'] != sender]

    def send(self, sender, data) -> None:
        self.add_sender(sender, data)

    def receive(self) -> bool:
        if len(self.provider_list) > 0:
            first_sender_dict = self.provider_list[0] # TODO: get random sender
            first_sender = first_sender_dict['sender']
            self.remove_sender(first_sender)
            first_sender.notify_sent()
            return first_sender_dict['data']
        return None
    

class CommRegister():
    def __init__(self, communication:Communication, bot) -> None:
        self.name = 'M'
        self.communication = communication
        self.bot = bot
        self.data = None
        self.is_local = False

    def read(self):
        data = self.communication.receive()
        if data is None:
            self.bot.set_comm_blocked(True)
            return None
        else:
            self.bot.set_comm_blocked(False)
            return data

    def write(self, data):
        self.communication.send(self, data)
        self.data = data
        self.bot.set_comm_blocked(True)

    def notify_sent(self):
        self.bot.set_comm_blocked(False)
        self.data = None

    def __repr__(self) -> str:
        return f"Data: {self.data}, is_local: {self.is_local}"

globalComm = Communication()