import random

import pytest

from Game.domain.tournament import Tournament

IDS = ["assassino", "cavaleiro", "mago"]


def make():
    return Tournament("mago", IDS, random.Random(1))


def test_opponents_exclude_player_and_cover_everyone():
    t = make()
    assert sorted(t.opponents) == ["assassino", "cavaleiro"]
    assert t.total_rounds == 2 and t.round_number == 1


def test_win_all_rounds_makes_champion():
    t = make()
    first = t.current_opponent
    t.record(True)
    assert not t.is_over and t.round_number == 2 and t.current_opponent != first
    t.record(True)
    assert t.is_over and t.is_champion and t.current_opponent is None


def test_loss_eliminates_immediately():
    t = make()
    t.record(False)
    assert t.is_over and t.eliminated and not t.is_champion


def test_cannot_record_after_end():
    t = make()
    t.record(False)
    with pytest.raises(RuntimeError):
        t.record(True)


def test_needs_opponent():
    with pytest.raises(ValueError):
        Tournament("mago", ["mago"])


def test_max_rounds_caps_opponents_and_arenas():
    ids = ["a", "b", "c", "d", "e", "f"]
    t = Tournament("a", ids, random.Random(1), ["x", "y", "z", "w"], max_rounds=4)
    assert t.total_rounds == len(t.opponents) == len(t.arenas) == 4
    assert "a" not in t.opponents and set(t.arenas) == {"x", "y", "z", "w"}
