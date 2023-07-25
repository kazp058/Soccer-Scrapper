from src.modules.Scrapper.Scrapper import Scrapper
from src.modules.Scrapper.Scrapper import Objective as scp_obj
from src.modules.FileManager.FileManager import FileManager
from src.modules.FileManager.FileManager import Objective as fm_obj

class Distance:

    __FILENAME = "distances"
    __DISTANCES = []

    def __init__(self, location_a:str = None, location_b:str = None) -> None:
        self.location_a = location_a
        self.location_b = location_b
        self.distance = None
        self.time = None

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Distance):
            return False

        if __value.location_a == self.location_a and __value.location_b == self.location_b:
            return True
        
        elif __value.location_a == self.location_b and __value.location_b == self.location_a:
            return True
        
        return False
    
    def __str__(self) -> str:
        return self.location_a + "|" + self.location_b + "|" + str(self.distance) + "|" + str(self.time)
    
    def __check_if_distance_exists(__value: any) -> bool:
        for distance in Distance.__DISTANCES:
            if distance == __value:
                return distance
        return None
    
    def add_distance(__value: any) -> bool:
        if not Distance.__check_if_distance_exists(__value):
            Distance.__DISTANCES.append(__value)
    
    def build_from_string(__value: str):
        __distance = __value.split("|")
        new_distance = Distance()
        new_distance.location_a = __distance[0]
        new_distance.location_b = __distance[1]
        new_distance.distance = float(__distance[2])
        new_distance.time = int(__distance[3])
        return new_distance
    
    def get_distances() -> list:
        return Distance.__DISTANCES
    
    def get_time(hours, minutes) -> int:
        hours = 0 if hours == None else int(hours)
        minutes = 0 if minutes == None else int(minutes)
        return minutes + hours * 60
    
    def read_cache(__cache:any):
        for line in __cache:
            current_distance = Distance.build_from_string(line)
            Distance.__DISTANCES.append(current_distance)

    def clean_cache() -> None:
        Distance.__DISTANCES = []

    def calculate(self) -> None:
        distance = Distance.__check_if_distance_exists(self)
        
        if distance != None:
            return distance
        else:
            if self.location_a == self.location_b:
                self.distance = 0
                self.time = 0
            else:
                scrapper = Scrapper(scp_obj.DISTANCE)
                result = scrapper.launch(objective=scp_obj.DISTANCE, address_a=self.location_a, address_b=self.location_b)[0]
                self.distance = float(result[0])
                self.time = int(result[1]) * 60 + int(result[2]) + 30
                Distance.add_distance(self)
                FileManager.save("distances",self,objective=fm_obj.OBJECT)
            return self
