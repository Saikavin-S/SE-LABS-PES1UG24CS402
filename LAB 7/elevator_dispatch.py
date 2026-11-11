"""Elevator dispatch helpers (hardened version).

Every function validates its input and returns None for anything malformed
(wrong type, missing separator, non-numeric parts, zero capacity, ...) instead
of crashing with an exception. Only plain ASCII integers of up to 9 digits are
accepted, which also blocks huge-number inputs and look-alike Unicode digits.
"""
import re

_INT_RE = re.compile(r"[+-]?[0-9]{1,9}")


def _to_int(part):
    """Return int for a clean integer string (surrounding spaces allowed), else None."""
    part = part.strip()
    if _INT_RE.fullmatch(part) is None:
        return None
    return int(part)


def parse_request(text):
    """'FROM->TO' -> (from, to), or None if the text is not a valid request."""
    if not isinstance(text, str):
        return None
    parts = text.split('->')
    if len(parts) != 2:
        return None
    start, end = _to_int(parts[0]), _to_int(parts[1])
    if start is None or end is None:
        return None
    return start, end


def total_travel(floors_csv):
    """'1,5,3,9' -> total floors travelled, or None if the CSV is invalid."""
    if not isinstance(floors_csv, str):
        return None
    floors = [_to_int(f) for f in floors_csv.split(',')]
    if any(f is None for f in floors):
        return None
    return sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))


def load_percent(text):
    """'450 of 630' -> 71, or None if invalid (bad format, negative load, capacity <= 0)."""
    if not isinstance(text, str):
        return None
    parts = text.split(' of ')
    if len(parts) != 2:
        return None
    load, capacity = _to_int(parts[0]), _to_int(parts[1])
    if load is None or capacity is None or load < 0 or capacity <= 0:
        return None
    return load * 100 // capacity


def main():
    print("==== Running parse_request ====")
    user_input = input("Enter a request as FROM->TO (e.g. 5->9): ")
    result = parse_request(user_input)
    print("From and To:", result if result is not None else "Invalid input")

    print("\n==== Running total_travel ====")
    user_input = input("Enter floors visited as CSV (e.g. 1,5,3,9): ")
    result = total_travel(user_input)
    print("Floors Travelled:", result if result is not None else "Invalid input")

    print("\n==== Running load_percent ====")
    user_input = input("Enter load as 'X of Y' (e.g. 450 of 630): ")
    result = load_percent(user_input)
    print("Load Percent:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
