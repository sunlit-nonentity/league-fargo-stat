from bs4 import BeautifulSoup

def get_standings(session):
    url = "https://leagues3.amsterdambilliards.com/team9ball/abc/individual_standings.php?foo=bar"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="tableteir2")
    if not table:
        print("❌ Could not find standings table.")
        return []

    players = []
    rows = table.find_all("tr")[1:]  # skip header row

    for row in rows:
        cols = [col.get_text(strip=True) for col in row.find_all("td")]
        if len(cols) >= 6:
            player = {
                "name": cols[0],
                "team": cols[1],
                "matches_played": int(cols[2]),
                "racks_won": int(cols[3]),
                "racks_lost": int(cols[4]),
                "win_percentage": float(cols[5].replace("%", ""))
            }
            players.append(player)

    print(f"📊 Parsed {len(players)} players from standings.")
    return players
