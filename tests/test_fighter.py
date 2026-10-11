import pytest

from Game.domain.actions import ActionType
from Game.domain.fighter import Assassin, Fighter, Knight, Mage


def test_defaults_per_class():
    assert (Assassin().physical, Assassin().magic) == (25, 15)
    assert (Knight().physical, Knight().magic) == (30, 10)
    assert (Mage().physical, Mage().magic) == (10, 35)


def test_defense_crit_and_mana_defaults():
    assert (Knight().physical_defense, Knight().magic_defense) == (8, 2)
    assert Assassin().crit_chance > Knight().crit_chance
    assert Mage().mana == Mage().max_mana and Mage().cost(ActionType.MAGIC) == 15


def test_mana_spend_and_regen_capped():
    m = Mage()
    m.spend_mana(15)
    assert m.mana == 15
    m.regen_mana()
    assert m.mana == 15 + Mage.MANA_REGEN
    for _ in range(10):
        m.regen_mana()
    assert m.mana == m.max_mana
    with pytest.raises(ValueError):
        m.spend_mana(m.max_mana + 1)


def test_magic_illegal_without_mana():
    m = Mage()
    m.spend_mana(m.mana)
    assert m.legal_actions() == [ActionType.PHYSICAL]


def test_invalid_crit_chance_rejected():
    with pytest.raises(ValueError):
        Fighter(crit_chance=1.5)


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
