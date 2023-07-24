import sys
from src.modules.Menu.Menu import Menu
from src.modules.Scrapper.Scrapper import Scrapper 
from src.modules.Scrapper.Scrapper import Objective as scrp_obj

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
        __cache = []
        for idx in range(len(App.__tournaments)):
            tournament = App.__tournaments[idx]
            url_pair = App.__url_pairs[idx]

            scrapper = Scrapper(url_pair= url_pair, 
                                tournament= tournament, 
                                objective=scrp_obj.MATCH)
            scrapper.launch(scrp_obj.MATCH)

    def __scrapper_paulista():
        __cache = []
        scrapper = Scrapper(url_pair= App.__url_pairs[0], 
                            tournament= App.__tournaments[0], 
                            objective=scrp_obj.MATCH)
        scrapper.launch(scrp_obj.MATCH)

    def __scrapper_gaucho():
        scrapper = Scrapper(url_pair= App.__url_pairs[1], 
                            tournament= App.__tournaments[1], 
                            objective=scrp_obj.MATCH)
        scrapper.launch(scrp_obj.MATCH)

    def __scrapper_mineiro():
        __cache = []
        scrapper = Scrapper(url_pair= App.__url_pairs[2],  
                            tournament= App.__tournaments[2], 
                            objective=scrp_obj.MATCH)
        scrapper.launch(scrp_obj.MATCH) 
           

    def __simulate():
        pass

    def __preload():
        pass

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