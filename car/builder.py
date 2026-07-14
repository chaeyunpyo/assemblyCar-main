from car.models import CarType, Engine, Brake, Steering
from car.rules import validate, first_violation

CAR_TYPE_NAMES = {
    CarType.SEDAN: "Sedan",
    CarType.SUV: "SUV",
    CarType.TRUCK: "Truck",
}

ENGINE_NAMES = {
    Engine.GM: "GM",
    Engine.TOYOTA: "TOYOTA",
    Engine.WIA: "WIA",
}

BRAKE_NAMES = {
    Brake.MANDO: "Mando",
    Brake.CONTINENTAL: "Continental",
    Brake.BOSCH: "Bosch",
}

STEERING_NAMES = {
    Steering.BOSCH: "Bosch",
    Steering.MOBIS: "Mobis",
}


def select_car_type(car, car_type):
    car.car_type = car_type
    return f"차량 타입으로 {CAR_TYPE_NAMES[car_type]}을 선택하셨습니다."


def select_engine(car, engine):
    car.engine = engine
    if engine == Engine.BROKEN:
        return "고장난 엔진을 선택하셨습니다."
    return f"{ENGINE_NAMES[engine]} 엔진을 선택하셨습니다."


def select_brake(car, brake):
    car.brake = brake
    return f"{BRAKE_NAMES[brake]} 제동장치를 선택하셨습니다."


def select_steering(car, steering):
    car.steering = steering
    return f"{STEERING_NAMES[steering]} 조향장치를 선택하셨습니다."


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
