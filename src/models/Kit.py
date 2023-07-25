import datetime

class Kit:
    TYPE_VAN = "VAN"
    TYPE_KIT = "KIT"

    VANS_COUNTER = 0
    KITS_COUNTER = 0

    __MATCH_DURANTION = 180
    __MIN_TIME_ALLOWED_KIT = 87120
    __MIN_TIME_ALLOWED_VAN = 480

    def __init__(self) -> None:
        self.id = None
        self.location = None
        self.until = None
        self.name = None
        self.type = None

    def setType(self, type:str):
        self.type = type

    def setUntil(self, timestamp):
        self.until = timestamp + datetime.timedelta(minutes=Kit.__MATCH_DURANTION)

    def setLocation(self, location: str):
        self.location = location

    def setId(self, id:int):
        self.id = id
        self.name = "KIT"+ str(int)

    def check_if_available(self, timestamp):
        if self.until == None:
            return True
        else:
            diff:datetime.datetime = timestamp - self.until
            if self.type == self.TYPE_KIT and diff.minutes >= self.__MIN_TIME_ALLOWED_KIT:
                return True
            elif self.type == self.TYPE_VAN and diff.minutes >= self.__MIN_TIME_ALLOWED_VAN:
                return True

    def __str__(self):
        return f"{self.until}({self.location})"