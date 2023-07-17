from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import re

import time

service = Service(executable_path="chromedriver.exe")

options = webdriver.ChromeOptions()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(
    # this will disable image loading
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

driver = webdriver.Chrome(service=service, options=options)

capture_date = r'([0-9]{2}\/[0-9]{2}\/[0-9]{4})'
capture_round = r'Jornada ([0-9]{1,2})'
capture_ko = r'KO ([0-9]{2}\:[0-9]{2})'
capture_stadium = r'Estadio ((Estádio )?[\w À-ÿ\d\.]*) \(.*\,'
capture_city = r'\(([\w À-ÿ]*)\,'
capture_state = r'\, ([\w À-ÿ]*)\)'

stack = []
score = r'[0-9] \- [0-9]'
reserved = ("FT", "Ver eventos","even aggr-even aggr","no-date-repetition-new","odd aggr-odd aggr")

btn_class = ''
btn = None

links = [("https://el.soccerway.com/national/brazil/paulista-a1/2023/regular-season/r68430/","https://el.soccerway.com/national/brazil/paulista-a1/2023/s21397/final-stages/"),
         ("https://el.soccerway.com/national/brazil/gaucho-1/2023/regular-season/r68315/","https://el.soccerway.com/national/brazil/gaucho-1/2023/s21374/final-stages/"),
         ("https://el.soccerway.com/national/brazil/mineiro-1/2023/regular-season/r68453/","https://el.soccerway.com/national/brazil/mineiro-1/2023/s21401/final-stages/")]

campeonatos = ["Paulista", "Gaucho", "Mineiro"]

#driver.get("https://el.soccerway.com/national/brazil/paulista-a1/2023/regular-season/r68430/")
#driver.get("https://el.soccerway.com/national/brazil/gaucho-1/2023/1st-phase/r68315/") matches   aggregates
#driver.get("https://el.soccerway.com/national/brazil/mineiro-1/2023/regular-season/r68453/")

for idx in range(len(links)):

    link_pair = links[idx]

    driver.get(link_pair[1])    
    WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'redesign'))
        )
    
    div_group = driver.find_elements(By.CSS_SELECTOR, 'div.block_competition_matches_full-wrapper')
    for div in div_group:
        current_round = div.find_element(By.CSS_SELECTOR, 'h2')
        
        matches = div.find_element(By.CSS_SELECTOR, 'table')
        tbody = matches.find_element(By.CSS_SELECTOR, 'tbody')
        tmatch = tbody.find_elements(By.CSS_SELECTOR, 'tr')
        for rmatch in tmatch:
                if rmatch.get_attribute("class") not in reserved:
                    info_match = rmatch.find_elements(By.CSS_SELECTOR, 'td')
                    teams = []
                    match_link = None
                    for info in info_match:
                        if re.search(score, info.text) != None:
                            link = info.find_element(By.CSS_SELECTOR, 'a')
                            match_link = link.get_attribute('href')
                        elif info.text not in reserved:
                            teams.append(info.text)
                    if match_link != None:
                        stack.append((tuple(teams), match_link, current_round.text))

    driver.get(link_pair[0])

    while btn_class != "previous disabled":
        
        if btn != None:
            btn.click()
            time.sleep(2)

        WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_element_located((By.ID, 'page_competition_1_block_competition_matches_summary_9'))
        )

        div = driver.find_element(By.ID, 'page_competition_1_block_competition_matches_summary_9')
        matches = div.find_element(By.CSS_SELECTOR, 'table')
        tbody = matches.find_element(By.CSS_SELECTOR, 'tbody')

        tmatch = tbody.find_elements(By.CSS_SELECTOR, 'tr')

        for rmatch in tmatch:
            if rmatch.get_attribute("class") != "no-date-repetition-new":
                info_match = rmatch.find_elements(By.CSS_SELECTOR, 'td')
                teams = []
                match_link = None
                for info in info_match:
                    if re.search(score, info.text) != None:
                        link = info.find_element(By.CSS_SELECTOR, 'a')
                        match_link = link.get_attribute('href')
                    elif info.text not in reserved:
                        teams.append(info.text)
                if match_link != None:
                    stack.append((tuple(teams), match_link, "null"))

        btn = driver.find_element(By.ID, "page_competition_1_block_competition_matches_summary_9_previous")
        btn_class = btn.get_attribute('class')

    
    print("partidos en total:", len(stack))
    write_counter = 0
    f = open(campeonatos[idx] + "_A1_2023.csv", "w", encoding="UTF-8")
    stack = stack[::-1]
    while len(stack) > 0:
        match = stack.pop(0)
        link = match[1]
        teams = match[0]
        driver.get(link)
        
        WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'details '))
        )

        details = driver.find_element(By.CLASS_NAME, "details ")
        date = re.search(capture_date, details.text).groups()[0] if re.search(capture_date, details.text) != None else "null"
        round = re.search(capture_round, details.text).groups()[0] if re.search(capture_round, details.text) != None else match[2]
        ko = re.search(capture_ko, details.text).groups()[0] if re.search(capture_ko, details.text) != None else "null"
        stadium = re.search(capture_stadium, details.text).groups()[0] if re.search(capture_stadium, details.text) != None else "null"     
        city = re.search(capture_city, details.text).groups()[0] if re.search(capture_city, details.text) != None else "null"
        state = re.search(capture_state, details.text).groups()[0] if re.search(capture_state, details.text) != None else "null"

        line = (round,
                teams[0],
                teams[1],
                city,
                state,
                stadium,
                date,
                ko
                )
        line = ",".join(line)
        print(line)
        f.write(line + '\n') 
        write_counter += 1

    f.close()
    btn_class = None
    btn = None
    print("Wrote for " + campeonatos[idx] + " " + str(write_counter) + " match(es).")
driver.quit()