from bs4 import BeautifulSoup

def get_team_id_from_standings(session, standings_url, team_name):
    response = session.get(standings_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for a in soup.find_all("a", href=True):
        link_text = a.get_text(strip=True)
        if (
            "team_scouting_report.php" in a["href"]
            and link_text
            and team_name.lower() in link_text.lower()
        ):
            href = a["href"]
            if "team_id=" in href:
                return href.split("team_id=")[-1]
    
    return None
