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
    
    def __check_if_distance_exists(__value: object) -> bool:
        for distance in Distance.__DISTANCES:
            if distance == __value:
                return True
        return False
    
    def add_distance(__value: str) -> bool:
        if not Distance.__check_if_distance_exists(__value):
            Distance.__DISTANCES.append(__value)
    
    def build_from_string(__value: str):
        __distance = __value.split("|")
        new_distance = Distance()
        new_distance.location_a = __distance[0]
        new_distance.location_b = __distance[1]
        new_distance.distance = __distance[2]
        new_distance.time = __distance[3]
        return new_distance
    
    def get_distances() -> list:
        return Distance.__DISTANCES
    
    def get_time(hours, minutes) -> int:
        hours = 0 if hours == None else int(hours)
        minutes = 0 if minutes == None else int(minutes)
        return minutes + hours * 60
    
    def read_cache(__cache:any):
        Distance.clean_cache()
        for line in __cache:
            current_distance = Distance.build_from_string(line)
            Distance.__DISTANCES.append(current_distance)

    def clean_cache() -> None:
        Distance.__DISTANCES = []

    def calculate() -> None:
        #llamar a scrapper para poder extraer la distancia
        pass