from car.models import Step

STEP_RANGES = {
    Step.CAR_TYPE: (1, 3),
    Step.ENGINE: (0, 4),
    Step.BRAKE: (0, 3),
    Step.STEERING: (0, 2),
    Step.FINAL: (0, 2),
}

ERROR_MESSAGES = {
    Step.CAR_TYPE: "ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능",
    Step.ENGINE: "ERROR :: 엔진은 1 ~ 4 범위만 선택 가능",
    Step.BRAKE: "ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능",
    Step.STEERING: "ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능",
    Step.FINAL: "ERROR :: Run 또는 Test 중 하나를 선택 필요",
}


def is_valid_range(step, ans):
    lo, hi = STEP_RANGES[step]
    return lo <= ans <= hi
