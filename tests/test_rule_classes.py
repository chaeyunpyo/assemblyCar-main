from car.models import Car, CarType, Engine, Brake, Steering
from car.rules.base import Rule
from car.rules.common import COMMON_RULES, BoschBrakeRequiresBoschSteering
from car.rules.type_specific import (
    TYPE_RULES,
    SedanRejectsContinentalBrake,
    SuvRejectsToyotaEngine,
    TruckRejectsWiaEngine,
    TruckRejectsMandoBrake,
)


def make_car(car_type=None, engine=None, brake=None, steering=None):
    return Car(car_type=car_type, engine=engine, brake=brake, steering=steering)


def test_all_rules_are_rule_instances():
    for rule in COMMON_RULES + TYPE_RULES:
        assert isinstance(rule, Rule)
        assert isinstance(rule.message, str) and rule.message


def test_bosch_brake_requires_bosch_steering_rule():
    rule = BoschBrakeRequiresBoschSteering()
    violated = make_car(CarType.SEDAN, Engine.GM, Brake.BOSCH, Steering.MOBIS)
    ok = make_car(CarType.SEDAN, Engine.GM, Brake.BOSCH, Steering.BOSCH)
    unrelated = make_car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.MOBIS)
    assert rule.is_violated(violated) is True
    assert rule.is_violated(ok) is False
    assert rule.is_violated(unrelated) is False


def test_sedan_rejects_continental_brake_rule():
    rule = SedanRejectsContinentalBrake()
    assert rule.is_violated(make_car(CarType.SEDAN, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)) is True
    assert rule.is_violated(make_car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.MOBIS)) is False
    assert rule.is_violated(make_car(CarType.SUV, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)) is False


def test_suv_rejects_toyota_engine_rule():
    rule = SuvRejectsToyotaEngine()
    assert rule.is_violated(make_car(CarType.SUV, Engine.TOYOTA, Brake.MANDO, Steering.MOBIS)) is True
    assert rule.is_violated(make_car(CarType.SUV, Engine.GM, Brake.MANDO, Steering.MOBIS)) is False


def test_truck_rejects_wia_engine_rule():
    rule = TruckRejectsWiaEngine()
    assert rule.is_violated(make_car(CarType.TRUCK, Engine.WIA, Brake.CONTINENTAL, Steering.MOBIS)) is True
    assert rule.is_violated(make_car(CarType.TRUCK, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)) is False


def test_truck_rejects_mando_brake_rule():
    rule = TruckRejectsMandoBrake()
    assert rule.is_violated(make_car(CarType.TRUCK, Engine.GM, Brake.MANDO, Steering.MOBIS)) is True
    assert rule.is_violated(make_car(CarType.TRUCK, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)) is False
