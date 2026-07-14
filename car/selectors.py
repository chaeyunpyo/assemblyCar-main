from car.models import Engine
from car.names import CAR_TYPE_NAMES, ENGINE_NAMES, BRAKE_NAMES, STEERING_NAMES


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
