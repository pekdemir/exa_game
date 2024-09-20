from enum import IntEnum

class CommState(IntEnum):
    IDLE = 0
    SEND_BLOCKED = 1
    SEND_SUCCESS = 2
    RECEIVE_BLOCKED = 3
    RECEIVE_SUCCESS = 4

class CommRegister():
    def __init__(self, communication):
        self.name = 'M'
        self.communication = communication
        self.is_local = False
        self.state = CommState.IDLE

    def read(self):
        return self.communication.receive()

    def write(self, data):
        if self.state == CommState.IDLE:
            self.communication.send(self, data)
            self.state = CommState.SEND_BLOCKED
        else:
            return False
    
    def notify_sended(self):
        self.state = CommState.IDLE



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
            first_sender = self.provider_list[0] # TODO: get random sender
            self.remove_sender(first_sender)
            return first_sender['data']
        return None