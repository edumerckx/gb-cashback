from collections import namedtuple

BonusRule = namedtuple('BonusRule', ['limit', 'bonus'])
bonus_rules = [
    BonusRule(1000, 0.1),
    BonusRule(1500, 0.15),
    BonusRule(float('inf'), 0.2),
]


def cashback(amount: float) -> tuple[float, float]:
    if amount <= 0:
        return 0, 0

    for rule in sorted(bonus_rules, key=lambda x: x.limit):
        if amount <= rule.limit:
            return amount * rule.bonus, rule.bonus * 100
