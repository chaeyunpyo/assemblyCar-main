from car.models import Car, CarType, Engine, Brake, Steering
from car.rules import validate


def make_car(car_type=None, engine=None, brake=None, steering=None):
    return Car(car_type=car_type, engine=engine, brake=brake, steering=steering)


# 제한조건 1: 부품 간 공통 호환성 (모든 차량 타입 공통)

def test_bosch_brake_requires_bosch_steering():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.BOSCH, Steering.MOBIS)
    violations = validate(car)
    assert any("Bosch" in v for v in violations)


def test_bosch_brake_with_bosch_steering_is_valid():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.BOSCH, Steering.BOSCH)
    violations = validate(car)
    assert not any("Bosch" in v for v in violations)


def test_bosch_brake_requires_bosch_steering_regardless_of_car_type():
    for car_type in (CarType.SEDAN, CarType.SUV, CarType.TRUCK):
        car = make_car(car_type, Engine.GM, Brake.BOSCH, Steering.MOBIS)
        violations = validate(car)
        assert any("Bosch" in v for v in violations), f"failed for {car_type}"


def test_non_bosch_brake_has_no_steering_restriction():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.MOBIS)
    violations = validate(car)
    assert not any("Bosch" in v for v in violations)


# 제한조건 2: 차량 타입별 부품 제한

def test_sedan_continental_incompatible():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)
    violations = validate(car)
    assert any("Continental" in v for v in violations)


def test_suv_toyota_incompatible():
    car = make_car(CarType.SUV, Engine.TOYOTA, Brake.MANDO, Steering.MOBIS)
    violations = validate(car)
    assert any("TOYOTA" in v for v in violations)


def test_truck_wia_incompatible():
    car = make_car(CarType.TRUCK, Engine.WIA, Brake.CONTINENTAL, Steering.MOBIS)
    violations = validate(car)
    assert any("WIA" in v for v in violations)


def test_truck_mando_incompatible():
    car = make_car(CarType.TRUCK, Engine.GM, Brake.MANDO, Steering.MOBIS)
    violations = validate(car)
    assert any("Mando" in v for v in violations)


def test_valid_sedan_combo_has_no_violations():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.BOSCH)
    assert validate(car) == []


def test_valid_suv_combo_has_no_violations():
    car = make_car(CarType.SUV, Engine.GM, Brake.MANDO, Steering.MOBIS)
    assert validate(car) == []


def test_multiple_violations_are_all_reported():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)
    # 위 조합은 Sedan+Continental 위반만 발생 (Continental != Bosch 이므로 규칙1은 위반 아님)
    # 규칙1과 동시 위반을 확인하려면 Bosch 브레이크로 규칙2 위반을 동시에 만들 수 없으므로
    # 서로 다른 두 규칙2 항목이 같이 위반되는 경우로 검증한다.
    car2 = make_car(CarType.TRUCK, Engine.WIA, Brake.MANDO, Steering.MOBIS)
    violations = validate(car2)
    assert any("WIA" in v for v in violations)
    assert any("Mando" in v for v in violations)
    assert len(violations) == 2
