import sqlite3
import argparse
from tabulate import tabulate

def connect_db(path="league_stats.db"):
    return sqlite3.connect(path)

def fetch_matches(conn, player_name=None):
    c = conn.cursor()

    if player_name:
        query = """
        SELECT date, team1, team2, player, opponent, player_racks, opponent_racks
        FROM matches
        WHERE player = ? OR opponent = ?
        ORDER BY date DESC
        """
        c.execute(query, (player_name, player_name))
    else:
        query = """
        SELECT date, team1, team2, player, opponent, player_racks, opponent_racks
        FROM matches
        ORDER BY date DESC
        """
        c.execute(query)

    return c.fetchall()

def summarize_player_stats(matches, player_name):
    total_matches = 0
    wins = 0
    racks_won = 0
    racks_lost = 0

    for match in matches:
        player = match[3]
        opponent = match[4]
        pr = match[5]
        orr = match[6]

        if player == player_name:
            total_matches += 1
            racks_won += pr
            racks_lost += orr
            if pr > orr:
                wins += 1
        elif opponent == player_name:
            total_matches += 1
            racks_won += orr
            racks_lost += pr
            if orr > pr:
                wins += 1

    win_pct = (wins / total_matches * 100) if total_matches > 0 else 0

    return {
        "total_matches": total_matches,
        "wins": wins,
        "win_pct": round(win_pct, 2),
        "racks_won": racks_won,
        "racks_lost": racks_lost
    }

def main():
    parser = argparse.ArgumentParser(description="Query match stats from the LeagueStat database")
    parser.add_argument("--player", help="Player name to filter by (e.g. 'Day Shanks')")
    args = parser.parse_args()

    conn = connect_db()
    matches = fetch_matches(conn, args.player)

    if not matches:
        print("No matches found.")
        return

    print(tabulate(matches, headers=["Date", "Team1", "Team2", "Player", "Opponent", "PR", "OR"], tablefmt="pretty"))

    if args.player:
        stats = summarize_player_stats(matches, args.player)
        print(f"\n📊 Stats for {args.player}:")
        print(f"Total Matches: {stats['total_matches']}")
        print(f"Wins: {stats['wins']}")
        print(f"Win %: {stats['win_pct']}%")
        print(f"Racks Won: {stats['racks_won']}")
        print(f"Racks Lost: {stats['racks_lost']}")

if __name__ == "__main__":
    main()
