import floor
import comm
import scheduler

class Globals:
    def __init__(self):
        self.floor = floor.Floor()
        self.communication = comm.Communication()
        self.scheduler = scheduler.Scheduler()

game_globals = Globals()