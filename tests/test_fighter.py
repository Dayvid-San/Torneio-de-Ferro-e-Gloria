import pytest

from Game.domain.actions import ActionType
from Game.domain.fighter import Assassin, Fighter, Knight, Mage


def test_defaults_per_class():
    assert (Assassin().physical, Assassin().magic) == (25, 15)
    assert (Knight().physical, Knight().magic) == (30, 10)
    assert (Mage().physical, Mage().magic) == (10, 35)


def test_take_damage_never_below_zero():
    f = Knight()
    assert f.take_damage(70) == 70
    assert f.take_damage(70) == 30
    assert f.hp == 0 and not f.is_alive


def test_negative_damage_is_ignored():
    f = Mage()
    assert f.take_damage(-5) == 0 and f.hp == f.max_hp


def test_invalid_stats_rejected():
    with pytest.raises(ValueError):
        Fighter(physical=0, magic=10)


def test_polymorphic_catchphrase():
    assert len({c().catchphrase() for c in (Assassin, Knight, Mage)}) == 3


def test_power_by_action():
    m = Mage()
    assert m.power(ActionType.MAGIC) == 35 and m.power(ActionType.PHYSICAL) == 10
