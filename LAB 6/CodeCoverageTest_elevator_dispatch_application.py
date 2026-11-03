import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---- next_direction (line coverage) ----
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"

def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"

def test_up_continues_up():
    assert next_direction(3, "up", [5]) == "up"

def test_up_reverses_to_down():
    assert next_direction(5, "up", [2]) == "down"

def test_up_nothing_left_goes_idle():
    assert next_direction(5, "up", []) == "idle"

def test_down_continues_down():
    assert next_direction(5, "down", [2]) == "down"

def test_down_reverses_to_up():
    assert next_direction(2, "down", [6]) == "up"

def test_down_nothing_left_goes_idle():
    assert next_direction(2, "down", []) == "idle"

def test_idle_picks_up():
    assert next_direction(2, "idle", [6]) == "up"

def test_idle_picks_down():
    assert next_direction(6, "idle", [2]) == "down"


# ---- door_action ----
def test_overload():
    assert door_action(700, False, False) == "overload"

def test_blocked_reopens():
    assert door_action(100, True, False) == "reopen"

def test_normal_close():
    assert door_action(100, False, False) == "close"


# ---- pick_elevator ----
def test_pick_nearest_idle_car():
    cars = [("A", 1, True), ("B", 8, True)]
    assert pick_elevator(cars, 7) == "B"
