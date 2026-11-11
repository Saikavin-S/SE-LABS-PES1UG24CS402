import re
from hypothesis import given, settings, strategies as st
from elevator_dispatch import parse_request, total_travel, load_percent

settings.register_profile("lab7", max_examples=500, deadline=None)
settings.load_profile("lab7")

# integers that fit the accepted format (at most 9 digits)
small_ints = st.integers(min_value=-999_999_999, max_value=999_999_999)
# things that are not strings at all
non_text = st.one_of(st.none(), st.integers(), st.floats(), st.booleans(),
                     st.lists(st.integers(), max_size=3), st.binary())


# ------------------------------------------------------------------ no-crash fuzzing
@given(st.text() | st.none())
def test_parse_request_no_crash(s):
    try:
        result = parse_request(s)
    except Exception as e:
        assert False, f"parse_request crashed with: {e!r} on input {s!r}"
    assert result is None or (
        isinstance(result, tuple) and len(result) == 2 and all(isinstance(x, int) for x in result)
    )


@given(st.text() | st.none())
def test_total_travel_no_crash(s):
    try:
        result = total_travel(s)
    except Exception as e:
        assert False, f"total_travel crashed with: {e!r} on input {s!r}"
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.text() | st.none())
def test_load_percent_no_crash(s):
    try:
        result = load_percent(s)
    except Exception as e:
        assert False, f"load_percent crashed with: {e!r} on input {s!r}"
    assert result is None or (isinstance(result, int) and result >= 0)


# ------------------------------------------------------------ correctness on valid input
@given(small_ints, small_ints)
def test_parse_request_roundtrip(a, b):
    assert parse_request(f"{a}->{b}") == (a, b)
    assert parse_request(f"  {a} ->  {b} ") == (a, b)


@given(st.lists(small_ints, min_size=1, max_size=30))
def test_total_travel_matches_definition(floors):
    csv = ",".join(str(f) for f in floors)
    expected = sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))
    assert total_travel(csv) == expected
    assert total_travel(csv) == total_travel(",".join(str(f) for f in reversed(floors)))


@given(st.integers(min_value=0, max_value=999_999_999),
       st.integers(min_value=1, max_value=999_999_999))
def test_load_percent_matches_definition(load, capacity):
    assert load_percent(f"{load} of {capacity}") == load * 100 // capacity


@given(st.integers(min_value=1, max_value=999_999_999))
def test_load_percent_full_car_is_100(capacity):
    assert load_percent(f"{capacity} of {capacity}") == 100


# --------------------------------------------------------------- invalid input is rejected
@given(small_ints, st.integers(max_value=0, min_value=-999_999_999) | st.just(0))
def test_load_percent_rejects_zero_or_negative_capacity(load, capacity):
    assert load_percent(f"{load} of {capacity}") is None      # was ZeroDivisionError / negative %


@given(st.integers(min_value=-999_999_999, max_value=-1), st.integers(min_value=1, max_value=10**6))
def test_load_percent_rejects_negative_load(load, capacity):
    assert load_percent(f"{load} of {capacity}") is None


@given(st.text().filter(lambda s: "->" not in s))
def test_parse_request_requires_arrow(s):
    assert parse_request(s) is None


@given(small_ints, small_ints, small_ints)
def test_parse_request_rejects_extra_arrows(a, b, c):
    assert parse_request(f"{a}->{b}->{c}") is None


@given(st.text(min_size=1, max_size=3).filter(
    lambda s: "," not in s and re.fullmatch(r"[+-]?[0-9]{1,9}", s.strip()) is None))
def test_total_travel_rejects_bad_element(junk):
    # a CSV containing a non-integer element must be rejected, never crash
    assert total_travel(f"1,{junk},3") is None


@given(st.integers(min_value=10**9, max_value=10**30))
def test_oversized_numbers_are_rejected(n):
    assert parse_request(f"{n}->1") is None
    assert total_travel(f"1,{n}") is None
    assert load_percent(f"{n} of 630") is None


def test_unicode_digits_are_rejected():
    assert parse_request("٣->4") is None          # Arabic-Indic digit three
    assert total_travel("1,٤") is None


@given(non_text)
def test_non_string_inputs_are_rejected(x):
    assert parse_request(x) is None
    assert total_travel(x) is None
    assert load_percent(x) is None
