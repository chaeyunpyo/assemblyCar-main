from car.models import Car, CarType, Engine, Brake, Steering
from car.service import CarAssemblyService


def test_select_car_type_sets_field_and_returns_message():
    service = CarAssemblyService()
    car = Car()
    msg = service.select_car_type(car, CarType.SEDAN)
    assert car.car_type == CarType.SEDAN
    assert "Sedan" in msg


def test_select_engine_broken_sets_field_and_returns_broken_message():
    service = CarAssemblyService()
    car = Car()
    msg = service.select_engine(car, Engine.BROKEN)
    assert car.engine == Engine.BROKEN
    assert "고장난 엔진" in msg


def test_select_brake_sets_field_and_returns_message():
    service = CarAssemblyService()
    car = Car()
    msg = service.select_brake(car, Brake.MANDO)
    assert car.brake == Brake.MANDO
    assert "Mando" in msg


def test_select_steering_sets_field_and_returns_message():
    service = CarAssemblyService()
    car = Car()
    msg = service.select_steering(car, Steering.BOSCH)
    assert car.steering == Steering.BOSCH
    assert "Bosch" in msg


def test_run_with_broken_engine_does_not_move():
    service = CarAssemblyService()
    car = Car(CarType.SEDAN, Engine.BROKEN, Brake.MANDO, Steering.BOSCH)
    lines = service.run(car)
    assert any("엔진이 고장나있습니다" in line for line in lines)
    assert any("자동차가 움직이지 않습니다" in line for line in lines)


def test_run_with_rule_violation_does_not_move():
    service = CarAssemblyService()
    car = Car(CarType.SEDAN, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)
    lines = service.run(car)
    assert lines == ["자동차가 동작되지 않습니다"]


def test_run_with_valid_combo_prints_parts_and_runs():
    service = CarAssemblyService()
    car = Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.BOSCH)
    lines = service.run(car)
    joined = "\n".join(lines)
    assert "Sedan" in joined
    assert "GM" in joined
    assert "Mando" in joined
    assert "Bosch" in joined
    assert "자동차가 동작됩니다" in joined


def test_test_pass_message():
    service = CarAssemblyService()
    car = Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.BOSCH)
    assert service.test(car) == "PASS"


def test_test_fail_message_reports_first_violation_in_original_order():
    service = CarAssemblyService()
    car = Car(CarType.TRUCK, Engine.WIA, Brake.MANDO, Steering.MOBIS)
    assert service.test(car) == "FAIL\nTruck에는 WIA엔진 사용 불가"


def test_service_accepts_injected_rules_for_testing():
    from car.rules.base import Rule

    class AlwaysViolated(Rule):
        message = "항상 위반"

        def is_violated(self, car):
            return True

    service = CarAssemblyService(rules=[AlwaysViolated()])
    car = Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.BOSCH)
    assert service.test(car) == "FAIL\n항상 위반"
