class Scheduler:
    def __init__(self) -> None:
        self.bots = []
        self.first_start = True

    def add_bot(self, bot) -> None:
        self.bots.append(bot)
    
    def cycle(self) -> bool:
        self.first_start = False
        stepped_bots = []
        while len(self.bots) > 0:
            current_bot = self.bots.pop(0)
            try:
                result = current_bot.step()
            except Exception as e:
                print(f"Bot ID: {current_bot.id} - {e}")  
                current_bot.destroy()
                continue
            if result:
                stepped_bots.append(current_bot)
        self.bots = stepped_bots
        if len(self.bots) == 0:
            return False
        return True

