from src.models.Match import Match
from src.models.Kit import Kit
from src.models.Distance import Distance
import datetime
from src.modules.FileManager.FileManager import FileManager
from src.modules.FileManager.FileManager import Objective as fm_obj
class Assignation():
    def __init__(self, match: Match, kit: Kit, distance:Distance) -> None:
        self.match: Match = match
        self.kit:Kit = kit
        self.distance: Distance = distance
    
    def __str__(self) -> str:
        stadium_a = self.distance.location_a.split(",")[0]
        stadium_b = self.distance.location_b.split(",")[0]
        travel_minutes = str(self.distance.time % 60) if self.distance.time % 60 >= 10 else "0" + str(self.distance.time % 60)
        travel_hours = self.distance.time // 60
        travel_time = str(travel_hours) + ":" + travel_minutes
        time_frame = str(self.kit.timeframe) if self.kit.timeframe != None else "0"
        return self.match.__str__() + "|" + self.kit.type + str(self.kit.id) + "|" + stadium_b + "->" + stadium_a + "|" + time_frame + "|" + travel_time

class By:
    PAULISTA = "Paulista"
    MINEIRO = "Mineiro"
    GAUCHO = "Gaucho"
    ALL = "ALL"

class Simulate():

    def launch(max_vans = 0, __matches = {}):
        FileManager.delete("simulation_result")
        for by in (By.PAULISTA, By.MINEIRO, By.GAUCHO, By.ALL):
            for i in range(max_vans + 1):
                kit_count = Simulate.simulate(i, __matches, by)
                line = by + "--> " + "vans: " + str(i) + " | kits: " + str(kit_count)
                FileManager.save("simulation_result", line, fm_obj.STRING)

    def simulate(vans:int = 0, __matches = {}, by = By.ALL):
        FileManager.delete("simulation_"+ by + "_" + str(vans) )
        kits_available:list[Kit] = []
        __KIT_COUNTER = 0

        assignation = []

        for van_idx in range(1,vans + 1):
            kits_available.append(Simulate.__create_van(van_idx))

        for __date in sorted(__matches.keys()):
            __pointer_date:dict = __matches[__date]
            for __ko in sorted(__pointer_date.keys()):
                __pointer_ko:dict = __pointer_date[__ko]
                for __match_id in __pointer_ko:
                    pointer_match:Match = __pointer_ko[__match_id]

                    if by == By.ALL or pointer_match.tournament == by:
                        tms = pointer_match.get_timestamp()

                        prefered = None
                        prefered_distance = None
                        for __kit in kits_available:
                            if __kit.location == pointer_match.get_address():
                                prefered = __kit
                                prefered_distance = Distance(__kit.location, pointer_match.get_address()).calculate()
                                break
                            if __kit.until != None and __kit.until > tms:
                                pass
                            else:
                                distance_pointer:Distance = Distance(__kit.location, pointer_match.get_address()).calculate()
                                time_window = tms - datetime.timedelta(minutes=distance_pointer.time)

                                if __kit.check_if_available(time_window):
                                    print(__kit.type, __kit.id ," available >>", __kit.location, __kit.until)
                                    if prefered == None:
                                        prefered = __kit
                                        prefered_distance = distance_pointer
                                        break
                                    else:
                                        if __kit.until == None and prefered.until != None:
                                            prefered = __kit
                                            prefered_distance = distance_pointer
                                        elif __kit.until < prefered.until and distance_pointer.distance < prefered_distance.distance:
                                            prefered = __kit
                                            prefered_distance = distance_pointer
                                        
                        if prefered == None:
                            new_kit = Simulate.__create_kit(__KIT_COUNTER + 1, pointer_match.get_address())
                            kits_available.append(new_kit)
                            print("kit created:", __KIT_COUNTER+1)
                            __KIT_COUNTER += 1
                            prefered = new_kit
                            prefered_distance = Distance(prefered.location, pointer_match.get_address()).calculate()
                        
                        prefered.location = pointer_match.get_address()
                        prefered.setUntil(tms)
                        new_assignation = Assignation(pointer_match, prefered, prefered_distance)
                        print(new_assignation)
                        FileManager.save("simulation_"+ by + "_" + str(vans) , new_assignation,fm_obj.OBJECT)
                        assignation.append(new_assignation)
        return __KIT_COUNTER

    def __create_van(van_idx):
        new_van = Kit()
        new_van.location = "Sao Paulo, Sao Paulo"
        new_van.setType(Kit.TYPE_VAN)
        new_van.setId(van_idx)
        new_van.until = None
        return new_van
    
    def __create_kit(kit_idx, location):
        new_kit = Kit()
        new_kit.location = location
        new_kit.setType(Kit.TYPE_KIT)
        new_kit.setId(kit_idx)
        new_kit.until = None
        return new_kit