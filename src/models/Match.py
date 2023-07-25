class Match:

    __MATCHES = {}

    def __init__(self, tournament = None, 
                 round = None, home = None, 
                 away = None, city = None, 
                 state = None, stadium = None, 
                 date = None, ko = None) -> None:
        self.tournament = tournament
        self.round = round
        self.home = home
        self.away = away
        self.city = city
        self.state = state
        self.stadium = stadium
        self.date = date
        self.ko = ko

    def build_from_string(string:str):
        match_info = string.split("|")
        new_match = Match()
        new_match.tournament = match_info[0]
        new_match.round = match_info[1]
        new_match.home = match_info[2]
        new_match.away = match_info[3]
        new_match.city = match_info[4]
        new_match.state = match_info[5]
        new_match.stadium = match_info[6]
        new_match.date = match_info[7]
        new_match.ko = match_info[8]
        return new_match

    def get_address(self) -> str:
        return self.stadium + ", " + self.city + ", " + self.state + ", Brazil"

    def get_cache()-> dict:
        return Match.__MATCHES
    
    def read_cache(__cache:any):
        for line in __cache:
            current_match = Match.build_from_string(line)

            home = current_match.home
            date = current_match.date
            ko = current_match.ko
            gameround = current_match.round

            date = date.split("/")
            date = int(date[2] + date[1] + date[0])
            
            ko = ko.split(":")
            ko = int(ko[0] + ko[1]) if len(ko) > 1 else 0

            by_date = Match.__MATCHES.get(date,{})
            by_ko = by_date.get(ko, {})
            
            match_id = gameround + "_" + home
            by_ko[match_id] = current_match
            
            by_date[ko] = by_ko
            
            Match.__MATCHES[date] = by_date

    def clean_cache():
        Match.__MATCHES = {}

    def put_matches(matches):
        Match.__MATCHES = matches

    def __str__(self) -> str:
        return "|".join([
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