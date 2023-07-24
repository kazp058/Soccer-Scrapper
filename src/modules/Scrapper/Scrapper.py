from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re
import time

class Objective:
    MATCH = "MATCH"
    DISTANCE = "DISTANCE"

class Scrapper:

    __capture_date = r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})'
    __capture_round = r'Jornada ([0-9]{1,2})'
    __capture_ko = r'KO ([0-9]{2}\:[0-9]{2})'
    __capture_stadium = r'Estadio ((Estádio )?[\w À-ÿ\d\.]*) \(.*\,'
    __capture_city = r'\(([\w À-ÿ]*)\,'
    __capture_state = r'\, ([\w À-ÿ]*)\)'
    __capture_score = r'[0-9] \- [0-9]'
    __capture_hour = r'(\d+)\n?hr'
    __capture_minutes = r'(\d+)\n?min'
    __reserved = ("FT", "Ver eventos","even aggr-even aggr","no-date-repetition-new","odd aggr-odd aggr")

    def __init__(self, url: str = None, url_pair: tuple = None, tournament: str = None,  objective = Objective.MATCH) -> None:
            self.objective = objective
            self.__cache = []
            self.stack = []
            if objective == Objective.MATCH:
                self.url_pair = tuple            
                self.tournament = tournament
                self.__filename = tournament + "_A1" 

            elif objective == Objective.DISTANCE:
                self.url = url
                self.__filename = ""

            service = Service(executable_path=".\\chromedriver.exe")
            options = webdriver.ChromeOptions()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option(
            # this will disable image loading
            "prefs", {"profile.managed_default_content_settings.images": 2}
            )

            self.driver = webdriver.Chrome(service=service, options=options)
    
    def launch(self, objective, address_a = None, address_b = None) -> any:
        
        if(objective== Objective.MATCH):
            self.__prepare_match()
            self.__extract_match()
            self.__die()
        elif(objective == Objective.DISTANCE):
            self.__gather_distances(address_a, address_b)
            self.__die()
        
        return self.__cache

    def __gather_distances(self, address_a, address_b):

        replace = {"Estádio Distrital do Jardim Inamar,São Paulo,São Paulo":"Inamar Disitrict Stadium",
                "Allianz Parque,São Paulo,São Paulo":"Allianz Parque, Av Francisco Matarazzo 1705, São Paulo, Brazil",
                "Estádio Dr. Oswaldo Teixeira Duarte,São Paulo,São Paulo":"Estádio Doutor Osvaldo Teixeira Duarte, São Paulo-SP, Brazil"}

        address_a = replace[address_a] if address_a in replace.keys() else address_a
        address_b = replace[address_b] if address_b in replace.keys() else address_b

        self.driver.get("https://www.bing.com/maps/directions")    
        WebDriverWait(driver=self.driver, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.directionsPanel'))
        )
        driving_box = self.driver.find_element(By.CSS_SELECTOR, "div.dirModes")
        car_btn = driving_box.find_element(By.CSS_SELECTOR, "a.dirBtnDrive")
        car_btn.click()
        container = self.driver.find_element(By.CSS_SELECTOR, "ul[role=list]")
        boxes = container.find_elements(By.CSS_SELECTOR, "li")
        c_box = boxes[0].find_element(By.CSS_SELECTOR, "input")
        #Rua Mauro de Prospero, 1203, Bragança Paulista - São Paulo, 12929, Brazil
        #Estádio Cícero Pompeu de Toledo,São Paulo,São Paulo
        c_box.send_keys(address_a)
        c_box = boxes[1].find_element(By.CSS_SELECTOR, "input")
        c_box.send_keys(address_b)

        buttonContainer = self.driver.find_element(By.CSS_SELECTOR,"div.drTimeGo")
        button = buttonContainer.find_element(By.CSS_SELECTOR, "a.dirBtnGo")
        time.sleep(3)
        button.click()
        time.sleep(10)
        WebDriverWait(driver=self.driver, timeout=5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.seeAllRoutesPanel'))
        )
        route_box = self.driver.find_element(By.CSS_SELECTOR, "li.drTitle")
        distancecss = route_box.find_element(By.CSS_SELECTOR, "div.distanceLine")

        time_box = route_box.find_element(By.CSS_SELECTOR, "table.drDurationTable")
        hours = re.search(Scrapper.__capture_hour,time_box.text).groups()[0] if re.search(Scrapper.__capture_hour,time_box.text) != None else None
        minutes = re.search(Scrapper.__capture_minutes, time_box.text).groups()[0]  if re.search(Scrapper.__capture_minutes, time_box.text) != None else None
        distance = re.search(r'^([\d\.]+) km', distancecss.text).groups()[0]  if re.search(r'^([\d\.]+) km', distancecss.text) != None else None
        
        self.__cache.append((distance, hours, minutes))
    
    def __prepare_match(self):
        btn_class = ''
        btn = None

        self.driver.get(self.url_pair[1])    
        WebDriverWait(driver=self.driver, timeout=5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'redesign'))
            )
        
        div_group = self.driver.find_elements(By.CSS_SELECTOR, 'div.block_competition_matches_full-wrapper')
        for div in div_group:
            current_round = div.find_element(By.CSS_SELECTOR, 'h2')
            
            matches = div.find_element(By.CSS_SELECTOR, 'table')
            tbody = matches.find_element(By.CSS_SELECTOR, 'tbody')
            tmatch = tbody.find_elements(By.CSS_SELECTOR, 'tr')
            for rmatch in tmatch:
                    if rmatch.get_attribute("class") not in Scrapper.__reserved:
                        info_match = rmatch.find_elements(By.CSS_SELECTOR, 'td')
                        teams = []
                        match_link = None
                        for info in info_match:
                            if re.search(Scrapper.__capture_score, info.text) != None:
                                link = info.find_element(By.CSS_SELECTOR, 'a')
                                match_link = link.get_attribute('href')
                            elif info.text not in Scrapper.__reserved:
                                teams.append(info.text)
                        if match_link != None:
                            self.stack.append((tuple(teams), match_link, current_round.text, self.tournament))
        self.driver.get(self.url_pair[0])

        while btn_class != "previous disabled":
            
            if btn != None:
                btn.click()
                time.sleep(2)

            WebDriverWait(driver=self.driver, timeout=5).until(
                EC.presence_of_element_located((By.ID, 'page_competition_1_block_competition_matches_summary_9'))
            )

            div = self.driver.find_element(By.ID, 'page_competition_1_block_competition_matches_summary_9')
            matches = div.find_element(By.CSS_SELECTOR, 'table')
            tbody = matches.find_element(By.CSS_SELECTOR, 'tbody')

            tmatch = tbody.find_elements(By.CSS_SELECTOR, 'tr')

            for rmatch in tmatch:
                if rmatch.get_attribute("class") != "no-date-repetition-new":
                    info_match = rmatch.find_elements(By.CSS_SELECTOR, 'td')
                    teams = []
                    match_link = None
                    for info in info_match:
                        if re.search(Scrapper.__capture_score, info.text) != None:
                            link = info.find_element(By.CSS_SELECTOR, 'a')
                            match_link = link.get_attribute('href')
                        elif info.text not in Scrapper.__reserved:
                            teams.append(info.text)
                    if match_link != None:
                        self.stack.append((tuple(teams), match_link, "null", self.tournament))

            btn = self.driver.find_element(By.ID, "page_competition_1_block_competition_matches_summary_9_previous")
            btn_class = btn.get_attribute('class')
    def __extract_match(self):
        while len(self.stack) > 0:
            match = self.stack.pop(len(self.stack)-1)
            link = match[1]
            teams = match[0]
            tournament = match[3]
            self.driver.get(link)
            
            WebDriverWait(driver=self.driver, timeout=5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'details '))
            )

            details = self.driver.find_element(By.CLASS_NAME, "details ")
            date = re.search(Scrapper.__capture_date, details.text).groups()[0] if re.search(Scrapper.__capture_date, details.text) != None else "null"
            round = re.search(Scrapper.__capture_round, details.text).groups()[0] if re.search(Scrapper.__capture_round, details.text) != None else match[2]
            ko = re.search(Scrapper.__capture_ko, details.text).groups()[0] if re.search(Scrapper.__capture_ko, details.text) != None else "null"
            stadium = re.search(Scrapper.__capture_stadium, details.text).groups()[0] if re.search(Scrapper.__capture_stadium, details.text) != None else "null"     
            city = re.search(Scrapper.__capture_city, details.text).groups()[0] if re.search(Scrapper.__capture_city, details.text) != None else "null"
            state = re.search(Scrapper.__capture_state, details.text).groups()[0] if re.search(Scrapper.__capture_state, details.text) != None else "null"

            current_match = "|".join((tournament,
                                  round,
                                  teams[0],
                                  teams[1],
                                  city,
                                  state,
                                  stadium,
                                  date,
                                  ko))
            self.__cache.append(current_match)
        return self.__cache