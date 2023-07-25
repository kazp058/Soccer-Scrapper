import datetime

class Kit:
    TYPE_VAN = "VAN"
    TYPE_KIT = "KIT"

    VANS_COUNTER = 0
    KITS_COUNTER = 0

    __MATCH_DURATION = 180
    __MIN_TIME_ALLOWED_KIT = 3930
    __MIN_TIME_ALLOWED_VAN = 1170

    def __init__(self) -> None:
        self.id = None
        self.location = None
        self.until = None
        self.name = None
        self.type = None
        self.timeframe = None

    def setType(self, type:str):
        self.type = type

    def setUntil(self, timestamp):
        self.until = timestamp + datetime.timedelta(minutes=Kit.__MATCH_DURATION)

    def setLocation(self, location: str):
        self.location = location

    def setId(self, id:int):
        self.id = id
        self.name = "KIT"+ str(int)

    def check_if_available(self, timestamp):
        if self.until == None:
            self.timeframe = 0
            return True
        else:
            diff = timestamp - self.until
            if diff.days < 0:
                return False
            
            minutes = diff.total_seconds() // 60 
            self.timeframe = minutes // 60
            if self.type == self.TYPE_KIT and minutes >= self.__MIN_TIME_ALLOWED_KIT:
                return True
            elif self.type == self.TYPE_VAN and minutes >= self.__MIN_TIME_ALLOWED_VAN:
                return True

    def __str__(self):
        return "|".join((self.type + str(self.id), self.location, str(self.until) ))