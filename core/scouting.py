import requests
from bs4 import BeautifulSoup

def get_match_history(session: requests.Session, scouting_url: str):
    response = session.get(scouting_url)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="tableteir2")
    matches = []

    for table in tables:
        rows = table.find_all("tr")
        if len(rows) < 2:
            continue

        # extract team names and date from the first row
        header_cells = rows[0].find_all("td")
        if len(header_cells) < 2:
            continue

        team_info = header_cells[0].get_text(strip=True)
        date = header_cells[-1].get_text(strip=True)

        if " vs. " not in team_info:
            continue

        team1, team2 = team_info.split(" vs. ")

        # skip the header row and parse each matchup
        for row in rows[2:]:
            cols = row.find_all("td")
            if len(cols) != 6:
                continue

            player = cols[0].get_text(strip=True)
            player_racks = cols[2].get_text(strip=True)
            opponent = cols[3].get_text(strip=True)
            opponent_racks = cols[5].get_text(strip=True)

            # skip TOTALS or incomplete rows
            if player.upper() == "TOTALS" or not player or not opponent:
                continue

            try:
                matches.append({
                    "date": date,
                    "team1": team1,
                    "team2": team2,
                    "player": player,
                    "opponent": opponent,
                    "player_racks": int(player_racks),
                    "opponent_racks": int(opponent_racks)
                })
            except ValueError:
                continue  # skip rows with invalid integer conversion

    return matches

def get_team_matches(session, scouting_url):
    return get_match_history(session, scouting_url)
