import sqlite3

def init_db():
    conn = sqlite3.connect("league_stats.db")
    c = conn.cursor()

    # players table
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            name TEXT,
            class TEXT,
            t_h INTEGER,
            dbs INTEGER,
            game_wins INTEGER,
            game_losses INTEGER,
            game_total INTEGER,
            match_wins INTEGER,
            match_losses INTEGER,
            match_total INTEGER
        )
    ''')

    # matches table
    c.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week INTEGER,
            player TEXT,
            opponent TEXT,
            player_racks INTEGER,
            opponent_racks INTEGER,
            team_name TEXT,
            opponent_team TEXT,
            team_racks INTEGER,
            opponent_team_racks INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def insert_players(players):
    conn = sqlite3.connect("league_stats.db")
    c = conn.cursor()

    for p in players:
        c.execute('''
            INSERT INTO players (
                rank, name, class, t_h, dbs,
                game_wins, game_losses, game_total,
                match_wins, match_losses, match_total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(p["rank"] or 0),
            p["name"],
            p["class"],
            int(p["t_h"] or 0),
            int(p["dbs"] or 0),
            int(p["game_wins"] or 0),
            int(p["game_losses"] or 0),
            int(p["game_total"] or 0),
            int(p["match_wins"] or 0),
            int(p["match_losses"] or 0),
            int(p["match_total"] or 0)
        ))

    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(players)} players into the database.")

def insert_matches(matches):
    conn = sqlite3.connect("league_stats.db")
    c = conn.cursor()

    for m in matches:
        c.execute('''
            INSERT INTO matches (
                week, player, opponent, player_racks, opponent_racks,
                team_name, opponent_team, team_racks, opponent_team_racks
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            m["week"],
            m["player"],
            m["opponent"],
            m["player_racks"],
            m["opponent_racks"],
            m["team_name"],
            m["opponent_team"],
            m["team_racks"],
            m["opponent_team_racks"]
        ))

    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(matches)} matches into the database.")
