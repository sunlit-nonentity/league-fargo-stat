import boto3
import json
import os
import psycopg2
import requests
from bs4 import BeautifulSoup
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "team9_indy9_login"
    region_name = "us-east-2"
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        raise Exception(f"Secrets Manager error: {e}")

def login(session, username, password):
    login_url = "https://leagues3.amsterdambilliards.com/login.php"
    payload = {
        "user": username,
        "pwd": password,
        "redirect_url": "/team9ball/abc/index.php",
        "action": "LOGIN"
    }
    res = session.post(login_url, data=payload)
    if "Welcome Back to Team 9 Ball" not in res.text:
        raise Exception("Login failed")

def scrape_matches(session, season_id, team_id):
    url = f"https://leagues3.amsterdambilliards.com/team9ball/abc/team_scouting_report.php?season_id={season_id}&team_id={team_id}"
    res = session.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    matches = []

    for table in soup.find_all("table", class_="tableteir2"):
        header = table.find("tr")
        if not header:
            continue
        cells = header.find_all("td")
        if len(cells) < 2:
            continue

        match_title = cells[0].get_text(strip=True)
        date = cells[1].get_text(strip=True)

        for row in table.find_all("tr")[2:]:
            cols = row.find_all("td")
            if len(cols) != 6:
                continue

            player = cols[0].get_text(strip=True)
            opponent = cols[3].get_text(strip=True)
            pr = cols[2].get_text(strip=True)
            or_ = cols[5].get_text(strip=True)

            if player.lower() == "totals":
                continue

            matches.append({
                "date": date,
                "team_names": match_title,
                "player": player,
                "opponent": opponent,
                "pr": int(pr) if pr.isdigit() else 0,
                "or": int(or_) if or_.isdigit() else 0
            })

    return matches

def insert_into_db(match_data):
    conn = psycopg2.connect(
        host=os.environ["RDS_HOST"],
        port=5432,
        database="league_stats",
        user=os.environ["RDS_USER"],
        password=os.environ["RDS_PASS"]
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS match_results (
            id SERIAL PRIMARY KEY,
            date TEXT,
            team1 TEXT,
            team2 TEXT,
            player TEXT,
            opponent TEXT,
            pr INTEGER,
            or INTEGER
        );
    """)

    for match in match_data:
        team1, _, team2 = match["team_names"].partition(" vs. ")
        cur.execute("""
            INSERT INTO match_results (date, team1, team2, player, opponent, pr, or)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            match["date"], team1.strip(), team2.strip(),
            match["player"], match["opponent"],
            match["pr"], match["or"]
        ))

    conn.commit()
    cur.close()
    conn.close()

def lambda_handler(event=None, context=None):
    creds = get_secret()
    username = creds["username"]
    password = creds["password"]
    team = creds.get("team")

    season_id = 247
    team_id = 382

    with requests.Session() as session:
        login(session, username, password)
        match_data = scrape_matches(session, season_id, team_id)

    insert_into_db(match_data)

    return {
        "statusCode": 200,
        "body": f"Inserted {len(match_data)} matches for team {team}"
    }
