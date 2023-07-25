import os

class By:
    DATE = "DATE"
    HOUR = "HOUR"
    DATE_HOUR = "DATE_HOUR"
    TOURNAMENT_PAULISTA = "Paulista"
    TOURNAMENT_MINEIRO = "Mineiro"
    TOURNAMENT_GAUCHO = "Gaucho"

class Objective:
    MATCH = "MATCH"
    ADDRESSES = "ADDRESSES"
    DISTANCES = "DISTANCES"
    STRING = "STRING"
    OBJECT = "OBJECT"
    LIST = "LIST"
    DICT = "DICT"

class FileManager:
    
    __ENCODING = "UTF-8"
    __EXTENSION = ".csv"

    __FOLDER = ".\\data\\"

    def __check_folder() -> bool:
        if not os.path.exists(".\\" + FileManager.__FOLDER):
            os.makedirs(".\\" + FileManager.__FOLDER)
            return False
        return True
    
    def delete(__filename: str) -> None:
        try:
            if FileManager.__check_folder():
                os.remove(".\\" + FileManager.__FOLDER + __filename + FileManager.__EXTENSION)
        except FileNotFoundError:
            pass

    def save(__filename:str, __value: any, objective: str, by:any = None) -> None:

        try:
            FileManager.__check_folder()
            with open(FileManager.__FOLDER + 
                      __filename + FileManager.__EXTENSION, "a", 
                      encoding= FileManager.__ENCODING) as file:
                if objective == Objective.STRING:
                    file.write(__value + "\n")
                elif objective == Objective.OBJECT:
                    file.write(__value.__str__() + "\n")
                elif objective == Objective.LIST:
                    for obj in __value:
                        file.write(obj.__str__() + "\n")
                elif objective == Objective.DICT:
                    for __date in sorted(__value.keys()):
                        __pointer_date:dict = __value[__date]
                        for __ko in sorted(__pointer_date.keys()):
                            __pointer_ko:dict = __pointer_date[__ko]
                            for __match_id in __pointer_ko:
                                pointer_match:object = __pointer_ko[__match_id]
                                line:str = pointer_match.__str__()
                                if by ==  None:
                                    file.write(pointer_match.__str__() + "\n")
                                elif by in line.split("|"):
                                    file.write(pointer_match.__str__() + "\n")
                                
        except FileNotFoundError:
            with open(FileManager.__FOLDER + __filename + 
                      FileManager.__EXTENSION, "w", 
                      encoding=FileManager.__ENCODING) as file:
                if objective == Objective.STRING:
                    file.write(__value + "\n")
                elif objective == Objective.OBJECT:
                    file.write(__value.__str__() + "\n")
                elif objective == Objective.LIST:
                    for obj in __value:
                        file.write(obj.__str__() + "\n")
                elif objective == Objective.DICT:
                    for __date in sorted(__value.keys()):
                        __pointer_date:dict = __value[__date]
                        for __ko in sorted(__pointer_date.keys()):
                            __pointer_ko:dict = __pointer_date[__ko]
                            for __match_id in __pointer_ko:
                                pointer_match = __pointer_ko[__match_id]
                                line:str = pointer_match.__str__()
                                if by ==  None:
                                    file.write(pointer_match.__str__() + "\n")
                                elif by in line.split("|"):
                                    file.write(pointer_match.__str__() + "\n")  
                

    def open_file(__filename:str, objective = None, by:any = None) -> any:
        __cache = []

        try:
            with open(FileManager.__FOLDER + __filename + FileManager.__EXTENSION, "r", encoding=FileManager.__ENCODING) as f:
                for line in f.readlines():
                    current_line = line.strip()
                    if by == None:
                        __cache.append(current_line)
                    elif by in current_line.split("|"):
                        __cache.append(current_line)
            return __cache
        except FileNotFoundError:
            return __cache