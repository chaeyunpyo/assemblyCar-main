from car.models import Engine
from car.names import CAR_TYPE_NAMES, ENGINE_NAMES, BRAKE_NAMES, STEERING_NAMES
from car.rules import ALL_RULES, validate, first_violation
from car import selectors


class CarAssemblyService:
    """차량 조립 도메인의 단일 진입점.

    cli.py는 이 서비스 하나에만 의존하고, rules/names/selectors 등
    내부 모듈 구성은 알 필요가 없다 (ISP/DIP).
    """

    def __init__(self, rules=None):
        self._rules = ALL_RULES if rules is None else rules

    def select_car_type(self, car, car_type):
        return selectors.select_car_type(car, car_type)

    def select_engine(self, car, engine):
        return selectors.select_engine(car, engine)

    def select_brake(self, car, brake):
        return selectors.select_brake(car, brake)

    def select_steering(self, car, steering):
        return selectors.select_steering(car, steering)

    def run(self, car):
        if validate(car, self._rules):
            return ["자동차가 동작되지 않습니다"]
        if car.engine == Engine.BROKEN:
            return ["엔진이 고장나있습니다.", "자동차가 움직이지 않습니다."]
        return [
            f"Car Type : {CAR_TYPE_NAMES[car.car_type]}",
            f"Engine   : {ENGINE_NAMES[car.engine]}",
            f"Brake    : {BRAKE_NAMES[car.brake]}",
            f"Steering : {STEERING_NAMES[car.steering]}",
            "자동차가 동작됩니다.",
        ]

    def test(self, car):
        violation = first_violation(car, self._rules)
        if violation:
            return f"FAIL\n{violation}"
        return "PASS"
