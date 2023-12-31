import sys
from src.modules.Menu.Menu import Menu
from src.modules.Scrapper.Scrapper import Scrapper 
from src.modules.Scrapper.Scrapper import Objective as scrp_obj
from src.models.Match import Match
from src.models.Distance import Distance
from src.modules.FileManager.FileManager import FileManager
from src.modules.FileManager.FileManager import Objective as fm_obj
from src.modules.FileManager.FileManager import By as fm_by

from src.modules.Simulate.Simulate import Simulate
from src.modules.Simulate.Simulate import By as sim_by

class App:
    __url_pairs = [("https://el.soccerway.com/national/brazil/paulista-a1/2023/regular-season/r68430/",
                "https://el.soccerway.com/national/brazil/paulista-a1/2023/s21397/final-stages/"),
            
            ("https://el.soccerway.com/national/brazil/gaucho-1/2023/regular-season/r68315/",
            "https://el.soccerway.com/national/brazil/gaucho-1/2023/s21374/final-stages/"),

            ("https://el.soccerway.com/national/brazil/mineiro-1/2023/regular-season/r68453/",
            "https://el.soccerway.com/national/brazil/mineiro-1/2023/s21401/final-stages/")]

    __tournaments = ["Paulista", "Gaucho", "Mineiro"]

    def __kill_prog():
        sys.exit(0)

    def __scrapper_all():
        FileManager.delete("joint_A1")
        FileManager.delete("Paulista_A1")
        FileManager.delete("Gaucho_A1")
        FileManager.delete("Mineiro_A1")
        __cache = []
        for idx in range(len(App.__tournaments)):
            tournament = App.__tournaments[idx]
            url_pair = App.__url_pairs[idx]

            scrapper = Scrapper(url_pair= url_pair, 
                                tournament= tournament, 
                                objective=scrp_obj.MATCH)
            __cache = __cache + scrapper.launch(scrp_obj.MATCH)
            print("Loaded matches: " + str(len(__cache))) 
        Match.clean_cache()
        Match.read_cache(__cache)
        FileManager.save("joint_A1", Match.get_cache(),objective=fm_obj.DICT)
        FileManager.save("Gaucho_A1", Match.get_cache(),objective=fm_obj.DICT, by= fm_by.TOURNAMENT_GAUCHO)
        FileManager.save("Paulista_A1", Match.get_cache(),objective=fm_obj.DICT, by= fm_by.TOURNAMENT_PAULISTA)
        FileManager.save("Mineiro_A1", Match.get_cache(),objective=fm_obj.DICT, by= fm_by.TOURNAMENT_MINEIRO)
    def __scrapper_paulista():
        FileManager.delete("Paulista_A1")
        scrapper = Scrapper(url_pair= App.__url_pairs[0], 
                            tournament= App.__tournaments[0], 
                            objective=scrp_obj.MATCH)
        __cache = scrapper.launch(scrp_obj.MATCH)
        print("Loaded matches: " + str(len(__cache))) 
        Match.read_cache(__cache)
        FileManager.save("Paulista_A1", Match.get_cache(),objective=fm_obj.DICT, by= fm_by.TOURNAMENT_PAULISTA)

    def __scrapper_gaucho():
        FileManager.delete("Gaucho_A1")
        scrapper = Scrapper(url_pair= App.__url_pairs[1], 
                            tournament= App.__tournaments[1], 
                            objective=scrp_obj.MATCH)
        __cache = scrapper.launch(scrp_obj.MATCH)
        print("Loaded matches: " + str(len(__cache))) 
        Match.read_cache(__cache)
        FileManager.save("Gaucho_A1", Match.get_cache(),objective=fm_obj.DICT, by= fm_by.TOURNAMENT_GAUCHO)

    def __scrapper_mineiro():
        FileManager.delete("Mineiro_A1")
        scrapper = Scrapper(url_pair= App.__url_pairs[2],  
                            tournament= App.__tournaments[2], 
                            objective=scrp_obj.MATCH)
        __cache = scrapper.launch(scrp_obj.MATCH)
        print("Loaded matches: " + str(len(__cache))) 
        Match.read_cache(__cache)
        FileManager.save("Mineiro_A1", Match.get_cache(),objective=fm_obj.DICT, by= fm_by.TOURNAMENT_MINEIRO)
           

    def __simulate():
        Simulate.launch(4, Match.get_cache())
        pass

    def __preload():
        #load matches if available
        Match.clean_cache()
        Distance.clean_cache()
        __cache_MATCHES = FileManager.open_file("joint_A1")
        if len(__cache_MATCHES) == 0:
            __cache_MATCHES = []
            __cache_MATCHES += FileManager.open_file("Gaucho_A1")
            __cache_MATCHES += FileManager.open_file("Mineiro_A1")
            __cache_MATCHES += FileManager.open_file("Paulista_A1")

            Match.read_cache(__cache_MATCHES)
            FileManager.save("joint_A1", Match.get_cache(),objective=fm_obj.DICT)
        else:
            Match.read_cache(__cache_MATCHES)

        __cache_DISTANCES = FileManager.open_file("distances")
        Distance.read_cache(__cache_DISTANCES)
 
        print("Loaded distances: " + str(len(__cache_DISTANCES)))
        print("Loaded matches: " + str(len(__cache_MATCHES))) 


    def run():

        mainMenu = Menu(self_call= True,
                        linejump_before=1,
                        ask_option_str="Select an option")
        
        scrapperMenu = Menu(self_call= True,
                        linejump_before=1,
                        ask_option_str="Select an option")

        mainMenu.add_option("Launch scrapper", scrapperMenu.launch)
        mainMenu.add_option("Preload", App.__preload)
        mainMenu.add_option("Simulate", App.__simulate)
        mainMenu.add_option("Exit", App.__kill_prog)

        scrapperMenu.add_option("All tournaments", App.__scrapper_all)
        scrapperMenu.add_option("Paulista",App.__scrapper_paulista)
        scrapperMenu.add_option("Gaucho",App.__scrapper_gaucho)
        scrapperMenu.add_option("Mineiro", App.__scrapper_mineiro)

        scrapperMenu.add_option("Return to main menu", mainMenu.launch)

        mainMenu.launch()