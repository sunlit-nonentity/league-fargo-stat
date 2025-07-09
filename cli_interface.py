import json
import requests
from core import auth, standings, scouting, database

def load_config(path='config.json'):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    config = load_config()

    username = config.get('username')
    password = config.get('password')
    team_name = config.get('team_name')

    # start session
    session = requests.Session()

    print("🔐 Logging in...")
    logged_in = auth.login(session, username, password)

    if not logged_in:
        print("❌ Login failed. Check credentials.")
        return
    print("✅ Login successful.")

    # Skipping standings until implemented
    # print("📥 Fetching player stats...")
    # players = standings.get_players(session)
    # database.insert_players(players, username)
    # print(f"✅ Inserted {len(players)} players into the database.")

    # get team scouting report (match history)
    print("📥 Fetching match history...")

    # resolve team_id from standings page using team_name
    standings_url = "https://leagues3.amsterdambilliards.com/team9ball/abc/team_standings.php?season_id=247"
    team_id = standings.get_team_id_from_standings(session, standings_url, team_name)

    if not team_id:
        print(f"❌ Could not find team_id for team '{team_name}'")
        return

    scouting_url = f"https://leagues3.amsterdambilliards.com/team9ball/abc/team_scouting_report.php?season_id=247&team_id={team_id}"
    matches = scouting.get_team_matches(session, scouting_url)

    print(f"🧪 Found {len(matches)} matches before inserting.")
    conn = database.init_db()
    inserted = database.insert_matches(conn, matches)
    print(f"✅ Inserted {inserted} matches into the database.")


if __name__ == "__main__":
    main()
