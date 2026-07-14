from car.models import Engine
from car.rules import validate, first_violation
from car.names import CAR_TYPE_NAMES, ENGINE_NAMES, BRAKE_NAMES, STEERING_NAMES
from car.selectors import select_car_type, select_engine, select_brake, select_steering

__all__ = [
    "select_car_type",
    "select_engine",
    "select_brake",
    "select_steering",
    "run",
    "test_car",
]


def run(car):
    if validate(car):
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


def test_car(car):
    violation = first_violation(car)
    if violation:
        return f"FAIL\n{violation}"
    return "PASS"
