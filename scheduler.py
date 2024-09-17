from bot import Bot, Code

class Scheduler:
    def __init__(self) -> None:
        self.bots = []
        self.blocked_bots = []
        self.current_bot = None

    def add_bot(self, bot: Bot) -> None:
        self.bots.append(bot)
    
    def cycle(self) -> bool:
        stepped_bots = []
        while len(self.bots) > 0:
            self.current_bot = self.bots.pop(0)
            try:
                result = self.current_bot.step()
            except Exception as e:
                print(f"Bot ID: {self.current_bot.id} - {e}")  
                continue
            if result:
                stepped_bots.append(self.current_bot)
        self.bots = stepped_bots
        if len(self.bots) == 0:
            return False
        return True
       
        
