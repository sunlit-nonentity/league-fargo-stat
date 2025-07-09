import sqlite3

def init_db():
    conn = sqlite3.connect("league_stats.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            name TEXT PRIMARY KEY,
            team TEXT,
            matches_played INTEGER,
            racks_won INTEGER,
            racks_lost INTEGER,
            win_percentage REAL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            team1 TEXT,
            team2 TEXT,
            player TEXT,
            opponent TEXT,
            player_racks INTEGER,
            opponent_racks INTEGER,
            UNIQUE(date, team1, team2, player, opponent, player_racks, opponent_racks)
        )
    ''')

    conn.commit()
    return conn

def insert_players(conn, players):
    c = conn.cursor()
    inserted = 0
    for p in players:
        try:
            c.execute("INSERT OR IGNORE INTO players VALUES (?, ?, ?, ?, ?, ?)", (
                p["name"], p["team"], int(p["matches_played"]),
                int(p["racks_won"]), int(p["racks_lost"]),
                float(p["win_percentage"])
            ))
            inserted += c.rowcount
        except Exception as e:
            print(f"Error inserting player {p['name']}: {e}")

    conn.commit()
    return inserted

def insert_matches(conn, matches):
    c = conn.cursor()
    inserted = 0
    for m in matches:
        try:
            c.execute('''
                INSERT OR IGNORE INTO matches
                (date, team1, team2, player, opponent, player_racks, opponent_racks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                m["date"], m["team1"], m["team2"],
                m["player"], m["opponent"],
                m["player_racks"], m["opponent_racks"]
            ))
            inserted += c.rowcount
        except Exception as e:
            print(f"Error inserting match {m['player']} vs {m['opponent']}: {e}")

    conn.commit()
    return inserted
