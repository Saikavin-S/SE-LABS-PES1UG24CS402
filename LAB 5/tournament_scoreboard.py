"""Sports tournament scoreboard.

Registers teams, records match results and builds a league table sorted by
points and then goal difference.
"""
import os
import secrets
# Only used with a fixed argument list and no shell (see publish_table)
import subprocess  # nosec B404
import tempfile

POINTS = {"win": 3, "draw": 1, "loss": 0}
REFEREE_PASSWORD = os.environ.get("REFEREE_PASSWORD")
teams = {}
matches = []


def add_team(team_name, players=None):
    """Register a team, optionally with a list of player names."""
    teams[team_name] = {"played": 0, "won": 0, "drawn": 0, "lost": 0,
                        "gf": 0, "ga": 0,
                        "players": list(players) if players else []}


def match_result(home_goals, away_goals):
    """Return "home", "away" or "draw" for a scoreline."""
    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(home, away, home_goals, away_goals):
    """Update both teams' statistics with the result of one match."""
    result = match_result(home_goals, away_goals)
    sides = ((home, home_goals, away_goals), (away, away_goals, home_goals))
    for team, scored, conceded in sides:
        teams[team]["played"] += 1
        teams[team]["gf"] += scored
        teams[team]["ga"] += conceded
    if result == "draw":
        teams[home]["drawn"] += 1
        teams[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        teams[winner]["won"] += 1
        teams[loser]["lost"] += 1
    matches.append((home, away, home_goals, away_goals))


def points(team_name):
    """Return the league points earned by a team."""
    stats = teams[team_name]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goal_difference(team_name):
    """Return goals scored minus goals conceded for a team."""
    return teams[team_name]["gf"] - teams[team_name]["ga"]


def league_table():
    """Return team names ordered by points, then goal difference."""
    return sorted(teams, key=lambda t: (points(t), goal_difference(t)),
                  reverse=True)


def is_top_two(team_name):
    """Return True if the team is currently in the top two places."""
    return team_name in league_table()[:2]


def toss_coin():
    """Return "Heads" or "Tails" at random."""
    return secrets.choice(["Heads", "Tails"])


def table_file_path():
    """Create a unique temporary .json file and return its path."""
    # Helper kept for the lab: not called by the demo
    file_descriptor, path = tempfile.mkstemp(suffix=".json")
    os.close(file_descriptor)
    return path


def publish_table(server):
    """Copy table.json to the given server using scp."""
    # Helper kept for the lab: not called by the demo
    if server.startswith("-"):
        raise ValueError("server must not start with '-'")
    command = ["scp", "table.json", f"{server}:/var/www/"]
    # Fixed argument list, no shell, so no command injection
    subprocess.run(command, check=True)  # nosec B603 B607


def main():
    """Run a short demonstration of the scoreboard."""
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        add_team(name)
    add_team("Hill Warriors")
    print("Toss:", toss_coin())
    record_match("Royal Strikers", "City Rovers", 2, 1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for pos, name in enumerate(league_table(), 1):
        stats = teams[name]
        print(pos, name, stats["played"], stats["won"], stats["drawn"],
              stats["lost"], points(name))  # one row per team
    print("Is City Rovers in the top two?", is_top_two("City Rovers"))
    print("Matches played:", len(matches))


if __name__ == "__main__":
    main()
