import re
import requests
from bs4 import BeautifulSoup

def get_team_scouting_url(dashboard_html: str, team_name: str):
    soup = BeautifulSoup(dashboard_html, "html.parser")
    link = soup.find("a", string=team_name)
    if link:
        return "https://leagues3.amsterdambilliards.com" + link["href"]
    return None

def get_match_history(session: requests.Session, scouting_url: str):
    response = session.get(scouting_url)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="tableteir2")
    matches = []

    for table in tables:
        header = table.find_previous("h4")
        if not header:
            continue
        header_text = header.get_text(strip=True)

        # Extract date and teams from header like: "Nine Of Diamonds vs. Opponent - June 1, 2025"
        match = re.search(r"(.+?) vs. (.+?) - (.+)", header_text)
        if not match:
            continue

        team1, team2, date = match.groups()

        rows = table.find_all("tr")[1:]  # skip header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            player = cols[0].get_text(strip=True)
            opponent = cols[1].get_text(strip=True)
            score = cols[2].get_text(strip=True)

            score_match = re.match(r"(\d+)-(\d+)", score)
            if not score_match:
                continue

            player_racks, opponent_racks = score_match.groups()

            matches.append({
                "date": date,
                "team1": team1,
                "team2": team2,
                "player": player,
                "opponent": opponent,
                "player_racks": int(player_racks),
                "opponent_racks": int(opponent_racks)
            })

    return matches
