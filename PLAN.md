# assemble.py 리팩토링 계획

기준 문서: [SPEC.md](./SPEC.md)

## 1. 현재 구조의 문제점

- **전역 mutable 상태(`q0~q4`)**: 함수 간 암묵적 의존성이 생겨 테스트/재사용이 어려움.
- **매직 넘버 남용**: `1`, `2`, `3` 등이 차량 타입/부품을 의미하지만 상수(`SEDAN`, `GM`...)와 조건문이 분리돼 가독성이 낮음.
- **호환성 규칙 중복 구현**: `is_valid_check()`와 `test_produced_car()`에 SPEC.md의 제한조건 1·2가 각각 다르게(하나는 bool 리턴, 하나는 print) 두 번 구현됨 → 규칙 변경 시 두 곳을 동시에 고쳐야 하는 버그 유발 지점.
- **확장성 부족**: SPEC.md 1)에서 "차량 타입은 향후 추가될 수 있다"고 명시하지만, 현재 코드는 타입 추가 시 `show_menu`, `is_valid_range`, `select_car_type`, `run_produced_car` 등 여러 곳의 if/elif를 모두 고쳐야 함.
- **UI(입력/출력/딜레이)와 도메인 로직(선택/검증)이 뒤섞임**: `input()`, `print()`, `time.sleep()`이 로직 함수 안에 있어 순수 단위 테스트가 불가능(콘솔 mocking 필요).
- **테스트 코드 없음**.

## 2. 목표 구조

```
assemble.py            # 진입점 (main만 남김, cli.py 호출)
car/
  __init__.py
  models.py             # CarType, Engine, Brake, Steering Enum + Car dataclass
  rules.py              # 제한조건 1(공통 호환성) / 제한조건 2(타입별 제한) — 단일 소스
  builder.py            # 선택/검증/조립 로직 (순수 함수, 전역 상태 없음)
cli.py                  # 메뉴 출력, input 루프, delay 등 UI 전용
tests/
  test_rules.py
  test_builder.py
  test_input_validation.py
```

- 전역 변수 `q0~q4` 제거 → `Car` dataclass(`car_type`, `engine`, `brake`, `steering`)로 대체.
- **제한조건 1**(공통 부품 간 호환 규칙)과 **제한조건 2**(타입별 제한 규칙)를 SPEC.md 구조 그대로 `rules.py`에서 두 개의 리스트로 분리 관리 → 향후 "다른 브랜드 쌍" 공통 규칙이나 신규 차량 타입 규칙 추가 시 해당 리스트에 항목만 추가하면 되도록 설계.
- 부품명 매핑을 `Enum` + `dict`(예: `ENGINE_NAMES = {Engine.GM: "GM", ...}`)로 대체해 if/elif 반복 제거.
- CLI(`input`, `print`, `delay`)는 `cli.py`로 분리, `car/` 패키지는 순수 로직만 포함해 stdin/stdout 없이 단위 테스트 가능하게 함.

## 3. 단계별 진행 순서

1. `Enum` 정의 (`CarType`, `Engine`, `Brake`, `Steering`, `Step`) — 매직 넘버 제거.
2. `Car` dataclass 도입, 전역 변수 삭제.
3. `rules.py`에 SPEC.md 구조를 그대로 반영해 규칙 분리:
   ```python
   # 제한조건 1: 공통 호환성 규칙 (차량 타입 무관)
   COMMON_RULES = [
       (lambda c: not (c.brake == Brake.BOSCH and c.steering != Steering.BOSCH),
        "Bosch제동장치에는 Bosch조향장치 이외 사용 불가"),
   ]

   # 제한조건 2: 차량 타입별 제한 규칙
   TYPE_RULES = [
       (lambda c: not (c.car_type == CarType.SEDAN and c.brake == Brake.CONTINENTAL),
        "Sedan에는 Continental제동장치 사용 불가"),
       (lambda c: not (c.car_type == CarType.SUV and c.engine == Engine.TOYOTA),
        "SUV에는 TOYOTA엔진 사용 불가"),
       (lambda c: not (c.car_type == CarType.TRUCK and c.engine == Engine.WIA),
        "Truck에는 WIA엔진 사용 불가"),
       (lambda c: not (c.car_type == CarType.TRUCK and c.brake == Brake.MANDO),
        "Truck에는 Mando제동장치 사용 불가"),
   ]

   def validate(car) -> list[str]:
       rules = COMMON_RULES + TYPE_RULES
       return [msg for cond, msg in rules if not cond(car)]
   ```
4. `is_valid_check()` / `test_produced_car()`를 `validate()` 하나로 통합, 결과 표시(PASS/FAIL, 동작 여부)만 다르게 처리.
5. 입력 검증(`is_valid_range`)을 `Step`별 허용 범위 `dict`로 데이터화.
6. `run_produced_car`, `test_produced_car`의 출력 로직을 `NAMES` 매핑 dict로 단순화.
7. CLI 루프(`main`)를 `cli.py`로 이동, `car/builder.py`의 순수 함수만 호출하도록 정리.
8. 각 단계마다 기존 동작(문구, 순서, PASS/FAIL 메시지)이 바뀌지 않는지 회귀 확인.
9. `tests/` 작성 및 `pytest` 실행.

## 4. 테스트 케이스

### 4-1. 제한조건 1 — 공통 호환성 규칙 (`test_rules.py`)

| # | 조건 | 기대 결과 |
|---|------|-----------|
| 1 | 제동장치 = Bosch, 조향장치 = Mobis (타사) | 위반: "Bosch제동장치에는 Bosch조향장치 이외 사용 불가" |
| 2 | 제동장치 = Bosch, 조향장치 = Bosch | 위반 없음 |
| 3 | 제동장치 = Mando(비Bosch), 조향장치 = Mobis | 위반 없음 (규칙 대상 아님) |

### 4-2. 제한조건 2 — 차량 타입별 제한 규칙 (`test_rules.py`)

| # | 조건 | 기대 결과 |
|---|------|-----------|
| 1 | Sedan + Continental 제동장치 | 위반: "Sedan에는 Continental제동장치 사용 불가" |
| 2 | SUV + Toyota 엔진 | 위반: "SUV에는 TOYOTA엔진 사용 불가" |
| 3 | Truck + WIA 엔진 | 위반: "Truck에는 WIA엔진 사용 불가" |
| 4 | Truck + Mando 제동장치 | 위반: "Truck에는 Mando제동장치 사용 불가" |
| 5 | Sedan + Mando + Bosch제동 + Bosch조향 (유효 조합) | 위반 없음 (PASS) |
| 6 | SUV + GM엔진 + Mando제동 + Mobis조향 (유효 조합) | 위반 없음 (PASS) |
| 7 | 여러 규칙 동시 위반 (Sedan+Continental, Bosch+Mobis) | 위반 메시지 2개 모두 포함 |

```python
def test_sedan_continental_incompatible():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.CONTINENTAL, Steering.MOBIS)
    violations = validate(car)
    assert any("Continental" in v for v in violations)

def test_bosch_brake_requires_bosch_steering_regardless_of_type():
    for car_type in (CarType.SEDAN, CarType.SUV, CarType.TRUCK):
        car = make_car(car_type, Engine.GM, Brake.BOSCH, Steering.MOBIS)
        violations = validate(car)
        assert any("Bosch" in v for v in violations)

def test_valid_combo_has_no_violations():
    car = make_car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.BOSCH)
    assert validate(car) == []
```

### 4-3. 빌더/조립 로직 (`test_builder.py`)

| # | 시나리오 | 기대 결과 |
|---|----------|-----------|
| 1 | `select_car_type(SEDAN)` 호출 | `car.car_type == CarType.SEDAN` |
| 2 | `select_engine(BROKEN)` (고장난 엔진) 선택 | `car.engine == Engine.BROKEN` |
| 3 | `run(car)` when `engine == BROKEN` | "엔진이 고장나있습니다" 결과, 동작 안 함 |
| 4 | `run(car)` when 규칙 위반 있음 | "자동차가 동작되지 않습니다" 결과 |
| 5 | `run(car)` when 유효 + 정상 엔진 | 각 부품 이름이 포맷된 결과 문자열에 포함 |

### 4-4. 입력 검증 (`test_input_validation.py`)

| # | step | 입력값 | 기대 결과 |
|---|------|--------|-----------|
| 1 | Step.CAR_TYPE | 0 | invalid |
| 2 | Step.CAR_TYPE | 1~3 | valid |
| 3 | Step.CAR_TYPE | 4 | invalid |
| 4 | Step.ENGINE | 0~4 | valid (0=뒤로가기 포함) |
| 5 | Step.ENGINE | 5 | invalid |
| 6 | Step.BRAKE | 0~3 | valid |
| 7 | Step.STEERING | 0~2 | valid |
| 8 | Step.FINAL | 0~2 | valid |
| 9 | Step.FINAL | 3 | invalid |

```python
@pytest.mark.parametrize("step,ans,expected", [
    (Step.CAR_TYPE, 0, False),
    (Step.CAR_TYPE, 1, True),
    (Step.CAR_TYPE, 3, True),
    (Step.CAR_TYPE, 4, False),
    (Step.ENGINE, 0, True),
    (Step.ENGINE, 4, True),
    (Step.ENGINE, 5, False),
])
def test_is_valid_range(step, ans, expected):
    assert is_valid_range(step, ans) == expected
```

### 4-5. (선택) CLI 통합 테스트

- `cli.py`의 `main()`은 `input()`을 monkeypatch하여 시나리오별(정상 완주, 뒤로가기, 잘못된 입력 후 재시도, `exit`)로 1~2개만 스모크 테스트로 커버. 도메인 로직은 4-1~4-4에서 이미 검증되므로 CLI 테스트는 "루프가 깨지지 않는지"만 확인.

## 5. 회귀 방지

- 리팩토링 전 현재 동작(메뉴 문구, 에러 메시지, PASS/FAIL 문구)을 그대로 유지 — 문자열 변경 없이 구조만 재배치.
- 각 단계 커밋마다 `pytest` 통과 확인 후 다음 단계로 진행.
