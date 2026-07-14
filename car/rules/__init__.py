from car.rules.common import COMMON_RULES
from car.rules.type_specific import TYPE_RULES

# 순서는 원본 assemble.py의 elif 체인과 동일하게 유지 (첫 번째 위반 메시지가
# test 화면의 FAIL 사유로 노출되므로 타입별 규칙 → 공통 규칙 순서가 중요하다)
ALL_RULES = TYPE_RULES + COMMON_RULES


def validate(car, rules=None):
    rules = ALL_RULES if rules is None else rules
    return [rule.message for rule in rules if rule.is_violated(car)]


def first_violation(car, rules=None):
    violations = validate(car, rules)
    return violations[0] if violations else None
