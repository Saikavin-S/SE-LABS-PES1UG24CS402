import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---- next_direction: every if evaluated True and False ----
@pytest.mark.parametrize("current, direction, requests, expected", [
    # direction == "up"
    (3, "up", [5], "up"),            # above True
    (3, "up", [5, 1], "up"),         # above preferred over below
    (5, "up", [2], "down"),          # above False, below True
    (5, "up", [], "idle"),           # above False, below False
    (5, "up", [5], "idle"),          # request on current floor ignored
    # direction == "down"
    (5, "down", [2], "down"),        # below True
    (5, "down", [2, 8], "down"),     # below preferred over above
    (2, "down", [6], "up"),          # below False, above True
    (2, "down", [], "idle"),         # below False, above False
    # direction == "idle" (or anything else)
    (2, "idle", [6], "up"),
    (6, "idle", [2], "down"),
    (3, "idle", [], "idle"),
    (3, "idle", [3], "idle"),
    (3, "idle", [1, 5], "up"),       # above wins when both exist
])
def test_next_direction(current, direction, requests, expected):
    assert next_direction(current, direction, requests) == expected


# ---- door_action: every if True and False ----
@pytest.mark.parametrize("load, blocked, emergency, expected", [
    (100, False, True, "hold_open"),
    (700, True, True, "hold_open"),     # emergency beats overload/blocked
    (700, False, False, "overload"),
    (700, True, False, "overload"),     # overload beats blocked
    (100, True, False, "reopen"),
    (100, False, False, "close"),
    (630, False, False, "close"),       # boundary: exactly 630 is not overload
    (631, False, False, "overload"),    # boundary: just above
])
def test_door_action(load, blocked, emergency, expected):
    assert door_action(load, blocked, emergency) == expected


# ---- pick_elevator: loop, idle penalty, best-is-None / gap<best_gap ----
def test_pick_nearest_idle_car():
    assert pick_elevator([("A", 1, True), ("B", 8, True)], 7) == "B"

def test_first_car_wins_when_later_is_farther():
    # second car evaluated, gap < best_gap False
    assert pick_elevator([("A", 4, True), ("B", 9, True)], 5) == "A"

def test_busy_car_penalised():
    # A is closer but busy (+5): gap 3+5=8 vs B idle gap 6
    assert pick_elevator([("A", 2, False), ("B", 11, True)], 5) == "B"

def test_tie_keeps_first_car():
    assert pick_elevator([("A", 3, True), ("B", 7, True)], 5) == "A"

def test_no_cars_returns_none():
    assert pick_elevator([], 5) is None

def test_single_busy_car_still_chosen():
    assert pick_elevator([("A", 1, False)], 4) == "A"
