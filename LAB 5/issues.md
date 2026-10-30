# Issues

Line numbers refer to the original `tournament_scoreboard.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Command injection via os.system (B605) | Security (High) | 71 | `os.system("scp table.json " + server + ...)` builds a shell command from a string, so a crafted `server` value can run arbitrary commands | Replaced with `subprocess.run(["scp", ...], check=True)`: a fixed argument list, no shell. Also reject server names starting with `-` so they cannot be read as scp options |
| Insecure temp file (B306) | Security (Medium) | 66 | `tempfile.mktemp` only returns a name, so another process can create that file first (race condition) | Used `tempfile.mkstemp`, which creates the file atomically, then closed the descriptor and returned the path |
| Hardcoded password (B105) | Security (Low) | 6 | `REFEREE_PASSWORD = "referee-demo"` stores a secret in source code | Read it from the `REFEREE_PASSWORD` environment variable |
| Non-cryptographic random (B311) | Security (Low) | 61 | `random.choice` is not suitable for security purposes | Switched to `secrets.choice` |
| Shared mutable default argument (W0102) | Logic bug | 11 | `players=[]` is created once, so all teams added without players share the same list | Default is now `None`, and each team gets its own new list |
| is_top_two can crash (R1714) | Logic bug | 56-58 | `table[0]` and `table[1]` raise IndexError when fewer than 2 teams exist | `team_name in league_table()[:2]` works for any number of teams |
| Demo runs on import | Quality | last line | `main()` ran whenever the module was imported | Added an `if __name__ == "__main__":` guard |
| Naming style (C0103) | Quality | 11-69 | camelCase functions and arguments (`addTeam`, `teamName`, `homeGoals`...) | Renamed everything to snake_case |
| Missing docstrings (C0114, C0116) | Quality | 1 and all functions | No module or function docstrings | Added docstrings |
| Unnecessary elif after return (R1705) | Quality | 17 | `elif` and `else` after `return` in `matchResult` | Used plain `if` statements |
| Whitespace before ':' (E203) | Style | 5 | `"win" : 3` | `"win": 3` |
| Blank lines (E302) | Style | 60 | Only one blank line before `tossCoin` | Two blank lines |
| Missing whitespace after ',' (E231) | Style | 79 | `2,1` | `2, 1` |
| Inline comment spacing (E261) | Style | 87 | One space before `# one row per team` | Two spaces |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.75/10 | 10.00/10 |
| Flake8 | 4 warnings | 0 warnings |
| Bandit | 4 findings (1 High, 1 Medium, 2 Low) | No issues, with `# nosec` comments on the subprocess lines explaining why they are safe |
