from gb_cashback.calculator import cashback


def test_cashback():
    assert cashback(0) == (0, 0)
    assert cashback(100) == (10, 10)
    assert cashback(1000) == (100, 10)
    assert cashback(1001) == (150.15, 15)
    assert cashback(1500) == (225, 15)
    assert cashback(1501) == (300.2, 20)
    assert cashback(2000) == (400, 20)
    assert cashback(10000) == (2000, 20)
