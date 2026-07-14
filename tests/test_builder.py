from car.models import Car, CarType, Engine, Brake, Steering
from car import builder


def test_select_car_type_sets_field_and_returns_message():
    car = Car()
    msg = builder.select_car_type(car, CarType.SEDAN)
    assert car.car_type == CarType.SEDAN
    assert "Sedan" in msg


def test_select_engine_broken_sets_field_and_returns_broken_message():
    car = Car()
    msg = builder.select_engine(car, Engine.BROKEN)
    assert car.engine == Engine.BROKEN
    assert "고장난 엔진" in msg


def test_select_brake_sets_field_and_returns_message():
    car = Car()
    msg = builder.select_brake(car, Brake.MANDO)
    assert car.brake == Brake.MANDO
    assert "MANDO" in msg or "Mando" in msg


def test_select_steering_sets_field_and_returns_message():
    car = Car()
    msg = builder.select_steering(car, Steering.BOSCH)
    assert car.steering == Steering.BOSCH
    assert "BOSCH" in msg or "Bosch" in msg


def test_run_with_broken_engine_does_not_move():
    car = Car(CarType.SEDAN, Engine.BROKEN, Brake.MANDO, Steering.BOSCH)
    lines = builder.run(car)
    assert any("엔진이 고장나있습니다" in line for line in lines)
    assert any("자동차가 움직이지 않습니다" in line for line in lines)


def test_run_with_rule_violation_does_not_move():
    car = Car(CarType.SEDAN, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)
    lines = builder.run(car)
    assert lines == ["자동차가 동작되지 않습니다"]


def test_run_with_valid_combo_prints_parts_and_runs():
    car = Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.BOSCH)
    lines = builder.run(car)
    joined = "\n".join(lines)
    assert "Sedan" in joined
    assert "GM" in joined
    assert "Mando" in joined or "Mando".upper() in joined
    assert "Bosch" in joined
    assert "자동차가 동작됩니다" in joined


def test_test_car_pass_message():
    car = Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.BOSCH)
    assert builder.test_car(car) == "PASS"


def test_test_car_fail_message_reports_first_violation_in_original_order():
    car = Car(CarType.TRUCK, Engine.WIA, Brake.MANDO, Steering.MOBIS)
    # 원본 코드 순서상 Truck+WIA 규칙이 Truck+Mando 규칙보다 먼저 검사된다
    assert builder.test_car(car) == "FAIL\nTruck에는 WIA엔진 사용 불가"


def test_test_car_fail_message_for_bosch_rule():
    car = Car(CarType.SEDAN, Engine.GM, Brake.BOSCH, Steering.MOBIS)
    assert builder.test_car(car) == "FAIL\nBosch제동장치에는 Bosch조향장치 이외 사용 불가"
