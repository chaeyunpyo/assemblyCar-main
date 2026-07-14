from car.models import CarType, Engine, Brake, Steering
from car.names import CAR_TYPE_NAMES, ENGINE_NAMES, BRAKE_NAMES, STEERING_NAMES


def test_car_type_names():
    assert CAR_TYPE_NAMES[CarType.SEDAN] == "Sedan"
    assert CAR_TYPE_NAMES[CarType.SUV] == "SUV"
    assert CAR_TYPE_NAMES[CarType.TRUCK] == "Truck"


def test_engine_names():
    assert ENGINE_NAMES[Engine.GM] == "GM"
    assert ENGINE_NAMES[Engine.TOYOTA] == "TOYOTA"
    assert ENGINE_NAMES[Engine.WIA] == "WIA"
    assert Engine.BROKEN not in ENGINE_NAMES


def test_brake_names():
    assert BRAKE_NAMES[Brake.MANDO] == "Mando"
    assert BRAKE_NAMES[Brake.CONTINENTAL] == "Continental"
    assert BRAKE_NAMES[Brake.BOSCH] == "Bosch"


def test_steering_names():
    assert STEERING_NAMES[Steering.BOSCH] == "Bosch"
    assert STEERING_NAMES[Steering.MOBIS] == "Mobis"
