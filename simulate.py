class Kit:
    def __init__(self) -> None:
        self.location = None
        self.until = None

    def setUntil(self, time: str):
        self.until = time

    def setLocation(self, location: str):
        self.location = location

    def __str__(self):
        return f"{self.until}({self.location})"
    
class Match:
    def __init__(self, tournament, round, home, away, city, 
                 state, stadium, date, ko) -> None:
        self.tournament = tournament
        self.round = round
        self.home = home
        self.away = away
        self.city = city
        self.state = state
        self.stadium = stadium
        self.date = date
        self.ko = ko
    
    def __str__(self) -> str:
        return ",".join([
                self.tournament,
                self.round,
                self.home,
                self.away,
                self.city,
                self.state,
                self.stadium,
                self.date,
                self.ko
            ])

f = open("joint_A1_2023.csv","r", encoding="UTF-8")
for line in f.readlines():
    pass