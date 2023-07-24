class Kit:
    TYPE_VAN = "VAN"
    TYPE_KIT = "KIT"

    VANS_COUNTER = 0
    KITS_COUNTER = 0

    __MIN_TIME_ALLOWED_KIT = 22000
    __MIN_TIME_ALLOWED_VAN = 200

    def __init__(self) -> None:
        self.id = None
        self.location = None
        self.until = None
        self.name = None
        self.type = None

    def setType(self, type:str):
        self.type = type

    def setUntil(self, time):
        self.until = time

    def setLocation(self, location: str):
        self.location = location

    def setId(self, id:int):
        self.id = id
        self.name = "KIT"+ str(int)

    def __str__(self):
        return f"{self.until}({self.location})"