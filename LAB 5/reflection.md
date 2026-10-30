# Reflection

## 1. Which issues were the easiest to fix and which were the hardest?

The Flake8 warnings were the easiest. There were only four, and each one told
me the exact line: a space before a colon, a missing blank line, a missing
space after a comma and a comment that needed two spaces. The Pylint naming
and docstring warnings were also easy, but there were many of them, and every
rename had to be applied at every call site.

The hardest were the security fixes, because they needed thought and not just
formatting. Replacing `os.system` meant building an argument list for
`subprocess.run`, and I also had to think about the server name being read as
a command-line option when it starts with `-`. Replacing `mktemp` with
`mkstemp` changed what the function returns internally, so I had to close the
file descriptor. Fixing the shared `players=[]` default also needed me to
understand how Python creates default values.

## 2. Did the tools report any false positives, or miss any real problems?

Bandit's B311 warning about `random.choice` is close to a false positive,
because a coin toss in a scoreboard is not security-sensitive. I still changed
it to `secrets.choice`, since that costs nothing. After I moved to
`subprocess`, Bandit warned about the import and the call (B404, B603, B607).
Here the code is safe: the arguments are a fixed list and no shell is used. So
I suppressed those with `# nosec` and a comment explaining the reason, instead
of leaving them unexplained.

The tools also missed things. `is_top_two` would crash with fewer than two
teams, because Pylint only suggested using `in` and never mentioned the
IndexError. Bandit saw the shell but not that a server name beginning with `-`
could be read as an option by scp. No tool checks that the league table is
correct. I only knew the output was right by working out the points by hand.

## 3. How does static analysis contribute to code quality and maintainability?

The Pylint score went from 4.75/10 to 10.00/10, Flake8 went from 4 warnings to
0, and Bandit went from 4 findings to none. The code is now consistent
(snake_case, PEP 8), documented, and safer: no shell command built from a
string, no predictable temp file, no password in the source. That makes it
easier to read and review, and the tools caught problems such as the shared
mutable default before the program was ever run.

## 4. How would you use static analysis in a real project, and what are its limits?

I would run Pylint, Flake8 and Bandit automatically on every commit or pull
request (a pre-commit hook or a CI step), and fail the build on any Bandit
High or Medium finding or on a Pylint score below a set threshold. Problems
found there are cheap to fix.

The limit is that these tools do not know what the program is supposed to do.
A clean report does not mean the code is correct, so static analysis has to be
combined with unit tests, code review and checking the output. Findings also
need judgement: each one should be fixed, or suppressed with a written reason,
as I did with the `# nosec` comments.
