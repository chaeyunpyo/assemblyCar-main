from car.models import Brake, Steering
from car.rules.base import Rule

# 제한조건 1: 부품 간 공통 호환성 (차량 타입 무관, 모든 기종 공통 적용)


class BoschBrakeRequiresBoschSteering(Rule):
    message = "Bosch제동장치에는 Bosch조향장치 이외 사용 불가"

    def is_violated(self, car) -> bool:
        return car.brake == Brake.BOSCH and car.steering != Steering.BOSCH


COMMON_RULES = [
    BoschBrakeRequiresBoschSteering(),
]
