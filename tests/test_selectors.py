from car.models import Car, CarType, Engine, Brake, Steering
from car import selectors


def test_select_car_type_sets_field_and_returns_message():
    car = Car()
    msg = selectors.select_car_type(car, CarType.SEDAN)
    assert car.car_type == CarType.SEDAN
    assert "Sedan" in msg


def test_select_engine_broken_sets_field_and_returns_broken_message():
    car = Car()
    msg = selectors.select_engine(car, Engine.BROKEN)
    assert car.engine == Engine.BROKEN
    assert "고장난 엔진" in msg


def test_select_engine_normal_sets_field_and_returns_message():
    car = Car()
    msg = selectors.select_engine(car, Engine.GM)
    assert car.engine == Engine.GM
    assert "GM" in msg


def test_select_brake_sets_field_and_returns_message():
    car = Car()
    msg = selectors.select_brake(car, Brake.MANDO)
    assert car.brake == Brake.MANDO
    assert "Mando" in msg


def test_select_steering_sets_field_and_returns_message():
    car = Car()
    msg = selectors.select_steering(car, Steering.BOSCH)
    assert car.steering == Steering.BOSCH
    assert "Bosch" in msg
