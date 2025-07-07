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

    # get player standings
    print("📥 Fetching player stats...")
    players = standings.get_players(session)
    database.insert_players(players, username)
    print(f"✅ Inserted {len(players)} players into the database.")

    # get team scouting report (match history)
    print("📥 Fetching match history...")
    matches = scouting.get_team_matches(session, team_name)
    print(f"🧪 Found {len(matches)} matches before inserting.")
    database.insert_matches(matches, username)
    print(f"✅ Inserted {len(matches)} matches into the database.")

if __name__ == "__main__":
    main()
