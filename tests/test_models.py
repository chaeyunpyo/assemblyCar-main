from car.models import CarType, Engine, Brake, Steering, Step


def test_car_type_members():
    assert CarType.SEDAN.value == 1
    assert CarType.SUV.value == 2
    assert CarType.TRUCK.value == 3


def test_engine_members():
    assert Engine.GM.value == 1
    assert Engine.TOYOTA.value == 2
    assert Engine.WIA.value == 3
    assert Engine.BROKEN.value == 4


def test_brake_members():
    assert Brake.MANDO.value == 1
    assert Brake.CONTINENTAL.value == 2
    assert Brake.BOSCH.value == 3


def test_steering_members():
    assert Steering.BOSCH.value == 1
    assert Steering.MOBIS.value == 2


def test_step_members():
    assert Step.CAR_TYPE.value == 0
    assert Step.ENGINE.value == 1
    assert Step.BRAKE.value == 2
    assert Step.STEERING.value == 3
    assert Step.FINAL.value == 4


def test_enums_are_distinct_types():
    # 같은 정수값이라도 Enum 타입이 다르면 서로 다른 값으로 취급되어야 한다
    assert CarType.SEDAN != Engine.GM
    assert Brake.BOSCH.value != Steering.BOSCH.value or Brake.BOSCH is not Steering.BOSCH
