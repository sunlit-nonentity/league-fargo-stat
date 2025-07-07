import argparse
import requests
import os
from dotenv import load_dotenv

from core.auth import login
from core.standings import get_standings
from core.scouting import get_team_scouting_url, get_match_history
from core.database import init_db, insert_players, insert_matches

# Load credentials
load_dotenv()

parser = argparse.ArgumentParser(description="LeagueStat CLI - Fetch and store Amsterdam Billiards data")
parser.add_argument("--team", type=str, required=True, help="Your exact team name (e.g. 'Nine Of Diamonds')")
args = parser.parse_args()

username = os.getenv("AMSTERDAM_USERNAME")
password = os.getenv("AMSTERDAM_PASSWORD")

session = requests.Session()
session, dashboard_html = login(session, username=username, password=password)

if not session or not dashboard_html:
    print("❌ Login failed. Please check your credentials.")
    exit(1)

print("✅ Login successful.")

# Initialize DB
db = init_db()

# Parse player standings and insert into DB
players = get_standings(session)
count = insert_players(db, players)
print(f"✅ Inserted {count} players into the database.")

# Parse match history and insert into DB
scouting_url = get_team_scouting_url(dashboard_html, args.team)
if not scouting_url:
    print(f"❌ Could not find scouting link for team '{args.team}'.")
    exit(1)

matches = get_match_history(session, scouting_url)
print(f"🧪 Found {len(matches)} matches before inserting.")
match_count = insert_matches(db, matches)
print(f"✅ Inserted {match_count} matches into the database.")
