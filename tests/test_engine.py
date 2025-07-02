import pytest
from mlm.engine import Partner, compute_commissions


def test_single_node():
    partners = [Partner(id=1, parent_id=None, monthly_revenue=3000)]
    result = compute_commissions(partners)
    assert result == {1: 0.0}


def test_simple_tree():
    partners = [
        Partner(id=1, parent_id=None, monthly_revenue=3000),
        Partner(id=2, parent_id=1, monthly_revenue=6000),
    ]
    result = compute_commissions(partners)
    # Partner 1 should earn 5% of partner 2's daily profit
    assert result[1] == round(0.05 * (6000 / 30), 2)
    assert result[2] == 0.0


def test_multi_level():
    partners = [
        Partner(id=1, parent_id=None, monthly_revenue=3000),
        Partner(id=2, parent_id=1, monthly_revenue=6000),
        Partner(id=3, parent_id=2, monthly_revenue=9000),
    ]
    result = compute_commissions(partners)
    daily2 = 6000 / 30
    daily3 = 9000 / 30
    # Partner 2 earns 5% of partner 3’s daily
    # Partner 1 earns 5% of both 2 and 3’s daily
    assert result[3] == 0.0
    assert result[2] == round(0.05 * daily3, 2)
    assert result[1] == round(0.05 * (daily2 + daily3), 2)


def test_cycle_detection():
    partners = [
        Partner(id=1, parent_id=None, monthly_revenue=100),  # root
        Partner(id=2, parent_id=1, monthly_revenue=100),
        Partner(id=3, parent_id=2, monthly_revenue=100),
        Partner(id=4, parent_id=3, monthly_revenue=100),
        Partner(id=5, parent_id=4, monthly_revenue=100),
        Partner(id=2, parent_id=5, monthly_revenue=100),  # cycle
    ]

    with pytest.raises(ValueError, match="Cycle detected"):
        compute_commissions(partners)


def test_nonexistent_parent():
    partners = [
        Partner(id=1, parent_id=99, monthly_revenue=1000),  # 99 does not exist
    ]
    with pytest.raises(ValueError, match="must have exactly one root"):
        compute_commissions(partners)


def test_multiple_roots():
    partners = [
        Partner(id=1, parent_id=None, monthly_revenue=100),
        Partner(id=2, parent_id=None, monthly_revenue=200),
    ]
    with pytest.raises(ValueError, match="must have exactly one root"):
        compute_commissions(partners)
