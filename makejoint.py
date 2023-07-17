names = [ "Paulista", "Gaucho","Mineiro"]
matches = {}

for name in names:
    f = open(name + "_A1_2023.csv", "r", encoding="UTF-8")
    for line in f.readlines():
        line  = line.strip().split(",")
        round = line[0]
        home = line[1]
        away = line[2]
        city = line[3]
        state = line[4]
        stadium = line[5]
        date = line[6]
        raw_date = line[6]
        raw_ko = line[7]
        ko = line[7]
        date = date.split("/")
        date = int(date[2] + date[1] + date[0])

        
        ko = ko.split(":")
        ko = int(ko[0] + ko[1]) if len(ko) > 1 else 0

        by_date = matches.get(date, {})
        by_ko = by_date.get(ko, {})
        
        match_id = round + "_" + home
        by_ko[match_id] = {
            "tournament": name,
            "round": round,
            "home": home,
            "away": away,
            "city": city,
            "state": state,
            "stadium": stadium,
            "date": raw_date,
            "ko": raw_ko
        }
        
        by_date[ko] = by_ko
        matches[date] = by_date
    f.close()
f = open("joint_A1_2023.csv","w", encoding="UTF-8")
for date in sorted(matches.keys()):
    current_date = matches[date]
    for ko in sorted(current_date.keys()):
        current_time = current_date[ko]
        for match_id in current_time.keys():
            match_pointer = current_time[match_id]
            line = [
                match_pointer["tournament"],
                match_pointer["round"],
                match_pointer["home"],
                match_pointer["away"],
                match_pointer["city"],
                match_pointer["state"],
                match_pointer["stadium"],
                match_pointer["date"],
                match_pointer["ko"]
            ]

            line = ",".join(line)
            f.write(line + "\n")
f.close()