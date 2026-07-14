from car.models import CarType, Engine, Brake, Steering

# 제한조건 1: 부품 간 공통 호환성 (차량 타입 무관, 모든 기종 공통 적용)
COMMON_RULES = [
    (
        lambda car: not (car.brake == Brake.BOSCH and car.steering != Steering.BOSCH),
        "Bosch제동장치에는 Bosch조향장치 이외 사용 불가",
    ),
]

# 제한조건 2: 차량 타입별 부품 제한
TYPE_RULES = [
    (
        lambda car: not (car.car_type == CarType.SEDAN and car.brake == Brake.CONTINENTAL),
        "Sedan에는 Continental제동장치 사용 불가",
    ),
    (
        lambda car: not (car.car_type == CarType.SUV and car.engine == Engine.TOYOTA),
        "SUV에는 TOYOTA엔진 사용 불가",
    ),
    (
        lambda car: not (car.car_type == CarType.TRUCK and car.engine == Engine.WIA),
        "Truck에는 WIA엔진 사용 불가",
    ),
    (
        lambda car: not (car.car_type == CarType.TRUCK and car.brake == Brake.MANDO),
        "Truck에는 Mando제동장치 사용 불가",
    ),
]


def validate(car):
    rules = COMMON_RULES + TYPE_RULES
    return [message for condition, message in rules if not condition(car)]
