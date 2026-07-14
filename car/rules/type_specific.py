from car.models import CarType, Engine, Brake
from car.rules.base import Rule

# 제한조건 2: 차량 타입별 부품 제한


class SedanRejectsContinentalBrake(Rule):
    message = "Sedan에는 Continental제동장치 사용 불가"

    def is_violated(self, car) -> bool:
        return car.car_type == CarType.SEDAN and car.brake == Brake.CONTINENTAL


class SuvRejectsToyotaEngine(Rule):
    message = "SUV에는 TOYOTA엔진 사용 불가"

    def is_violated(self, car) -> bool:
        return car.car_type == CarType.SUV and car.engine == Engine.TOYOTA


class TruckRejectsWiaEngine(Rule):
    message = "Truck에는 WIA엔진 사용 불가"

    def is_violated(self, car) -> bool:
        return car.car_type == CarType.TRUCK and car.engine == Engine.WIA


class TruckRejectsMandoBrake(Rule):
    message = "Truck에는 Mando제동장치 사용 불가"

    def is_violated(self, car) -> bool:
        return car.car_type == CarType.TRUCK and car.brake == Brake.MANDO


TYPE_RULES = [
    SedanRejectsContinentalBrake(),
    SuvRejectsToyotaEngine(),
    TruckRejectsWiaEngine(),
    TruckRejectsMandoBrake(),
]
