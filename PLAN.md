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

## 3. 단계별 진행 순서 (Phase 1~9, 완료)

1. ✅ `Enum` 정의 (`CarType`, `Engine`, `Brake`, `Steering`, `Step`) — 매직 넘버 제거.
2. ✅ `Car` dataclass 도입, 전역 변수 삭제.
3. ✅ `rules.py`에 SPEC.md 구조를 그대로 반영해 규칙 분리:
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
4. ✅ `is_valid_check()` / `test_produced_car()`를 `validate()` 하나로 통합, 결과 표시(PASS/FAIL, 동작 여부)만 다르게 처리.
5. ✅ 입력 검증(`is_valid_range`)을 `Step`별 허용 범위 `dict`로 데이터화.
6. ✅ `run_produced_car`, `test_produced_car`의 출력 로직을 `NAMES` 매핑 dict로 단순화 (`car/builder.py`).
7. ✅ CLI 루프(`main`)를 `cli.py`로 이동, `car/builder.py`의 순수 함수만 호출하도록 정리.
8. ✅ 각 단계마다 기존 동작(문구, 순서, PASS/FAIL 메시지)이 바뀌지 않는지 회귀 확인.
9. ✅ `tests/` 작성 및 `pytest` 실행 (63개 테스트, 전체 통과).

결과물: `car/models.py`(Enum+Car), `car/rules.py`(COMMON_RULES/TYPE_RULES+validate), `car/builder.py`(선택/실행/테스트 로직+이름 매핑), `car/validation.py`(입력 범위), `cli.py`(UI), `assemble.py`(진입점).

Phase 1~9로 매직 넘버·전역 상태·규칙 중복은 해소됐지만, `car/builder.py` 한 파일 안에 **이름 매핑(데이터) + 선택 로직(상태 변경) + run/test 오케스트레이션(비즈니스 로직)** 이 섞여 있다. 이 파일을 SOLID 원칙 기준으로 더 쪼갠다.

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

## 6. SOLID 원칙 기반 추가 파일 분리 (Phase 10~14, 완료)

### 현재(Phase 9까지) 남아있는 SOLID 위반 지점

| 원칙 | 위반 지점 | 문제 |
|---|---|---|
| **SRP** | `car/builder.py`가 이름 매핑(`*_NAMES` dict) + 선택 상태 변경(`select_*`) + run/test 오케스트레이션을 모두 담당 | 이름 표기만 바꾸고 싶어도, 선택 로직/조립 로직과 같은 파일을 건드려야 함 |
| **OCP** | `car/rules.py`의 규칙이 `(lambda, message)` 튜플로 표현되어 있어 "규칙에 우선순위/카테고리를 추가"하는 등 확장 시 튜플 구조 자체를 바꿔야 할 수 있음 | 규칙 객체가 아니라 익명 함수+문자열이라 개별 규칙 단위 테스트·재사용이 약함 |
| **LSP** | 규칙이 클래스가 아니므로 "치환 가능한 하위 타입" 관계 자체가 없음 | 향후 "조건이 여러 개인 규칙", "경고만 하고 차단은 안 하는 규칙" 등 변종이 생기면 자연스러운 확장이 어려움 |
| **ISP** | `cli.py`가 `car.builder`, `car.validation`, `car.models`를 모두 개별 import해서 필요한 것보다 넓은 표면에 의존 | UI 계층이 도메인 내부 구성(모듈 3개)에 대해 알아야 함 |
| **DIP** | `cli.py`(고수준 정책)가 `car.builder`/`car.validation`(저수준 구현) 모듈에 직접 의존 | 도메인 구현을 바꾸면 `cli.py`도 같이 바뀔 위험, 테스트 시 대체 구현 주입 불가 |

### 목표 구조

```
car/
  models.py         # (변경 없음) Enum + Car dataclass
  names.py          # NEW — 부품별 표시 이름 매핑만 (SRP: 이름 표기 담당)
  rules/
    __init__.py     # NEW — Rule 추상 클래스 + validate(car, rules) : OCP 기반 확장 지점
    common.py       # 제한조건 1 Rule 구현체 목록
    type_specific.py# 제한조건 2 Rule 구현체 목록
  selectors.py      # NEW — select_car_type/engine/brake/steering만 (SRP: 사용자의 선택 반영)
  service.py        # NEW — CarAssemblyService: rules+names+selectors를 조합해 run()/test()/select_*() 제공.
                     #        cli.py는 이 서비스 "하나"에만 의존 (DIP, ISP)
  validation.py     # (변경 없음)
cli.py              # CarAssemblyService 인스턴스 하나만 의존하도록 축소
```

### Phase 10 — `car/names.py` 분리 (SRP) ✅

- `car/builder.py`의 `CAR_TYPE_NAMES`, `ENGINE_NAMES`, `BRAKE_NAMES`, `STEERING_NAMES`를 `car/names.py`로 이동.
- 테스트 먼저: `tests/test_names.py`에 각 Enum 값이 대응하는 이름 문자열을 갖는지 검증 (예: `NAMES[CarType][CarType.SEDAN] == "Sedan"` 또는 개별 dict마다 확인).
- `car/builder.py`(이후 `selectors.py`/`service.py`)는 `car/names.py`를 import해서 사용.

### Phase 11 — `car/rules/` 를 `Rule` 클래스 기반으로 전환 (OCP, LSP) ✅

- 추상 인터페이스:
  ```python
  class Rule(ABC):
      message: str
      def is_violated(self, car: Car) -> bool: ...
  ```
- 기존 튜플 규칙을 `Rule`을 상속하는 개별 클래스(또는 동일 시그니처를 만족하는 작은 dataclass)로 변환:
  - `car/rules/common.py`: `BoschBrakeRequiresBoschSteering`
  - `car/rules/type_specific.py`: `SedanRejectsContinentalBrake`, `SuvRejectsToyotaEngine`, `TruckRejectsWiaEngine`, `TruckRejectsMandoBrake`
- `car/rules/__init__.py`:
  ```python
  ALL_RULES = COMMON_RULES + TYPE_RULES  # 각 모듈에서 인스턴스 리스트로 export

  def validate(car, rules=ALL_RULES) -> list[str]:
      return [r.message for r in rules if r.is_violated(car)]

  def first_violation(car, rules=ALL_RULES) -> str | None:
      violations = validate(car, rules)
      return violations[0] if violations else None
  ```
  - `rules` 파라미터에 기본값을 주되 주입 가능하게 하여, 신규 차량 타입/브랜드 규칙을 추가할 때 기존 `Rule` 클래스나 `validate()`를 수정하지 않고 새 `Rule` 인스턴스를 리스트에 추가하기만 하면 되도록 한다 (OCP). 순서는 기존과 동일하게 `TYPE_RULES + COMMON_RULES` 유지 (Phase 3~4에서 확인한 FAIL 메시지 우선순위 회귀 방지).
- 테스트: 기존 `tests/test_rules.py`의 케이스는 그대로 유지하되(동작 동일해야 함), 개별 `Rule` 클래스 단위 테스트를 추가해 각 규칙을 독립적으로 검증 (예: `SedanRejectsContinentalBrake().is_violated(car)`).

### Phase 12 — `car/selectors.py` 분리 (SRP) ✅

- `car/builder.py`의 `select_car_type`, `select_engine`, `select_brake`, `select_steering`을 `car/selectors.py`로 이동. `car/names.py`만 의존하도록 정리.
- 테스트: 기존 `tests/test_builder.py`의 `select_*` 관련 케이스를 `tests/test_selectors.py`로 이동/재작성.

### Phase 13 — `car/service.py` 도입 (DIP, ISP) ✅

- `run(car)`, `test_car(car)`를 `car/service.py`의 `CarAssemblyService`로 이동하고, 선택 메서드도 위임 형태로 노출:
  ```python
  class CarAssemblyService:
      def __init__(self, rules=ALL_RULES, names=NAMES):
          self._rules = rules
          self._names = names

      def select_car_type(self, car, car_type): ...
      def select_engine(self, car, engine): ...
      def select_brake(self, car, brake): ...
      def select_steering(self, car, steering): ...
      def run(self, car) -> list[str]: ...
      def test(self, car) -> str: ...
  ```
- `cli.py`는 더 이상 `car.builder`/`car.validation`/`car.rules`를 개별로 import하지 않고, `CarAssemblyService` 인스턴스 하나 + `car.validation.is_valid_range`(입력 검증은 UI 관심사이므로 별도 유지)만 사용하도록 축소한다. 즉 cli.py의 의존 표면을 "서비스 1개 + 입력 검증 1개"로 좁힌다 (ISP: UI가 도메인 내부 구조를 몰라도 되게, DIP: 저수준 모듈 대신 서비스 추상화에 의존).
- `car/builder.py`는 이 시점에 `car/names.py` + `car/selectors.py` + `car/service.py`로 완전히 대체되므로 삭제.
- 테스트: `tests/test_service.py`로 기존 `test_builder.py`의 run/test 관련 케이스를 이관, `CarAssemblyService`를 직접 생성해 검증. `tests/test_cli.py`는 구조 변경과 무관하게 동일한 시나리오로 계속 통과해야 함 (회귀 확인).

### Phase 14 — 최종 정리 및 회귀 확인 ✅

- `car/builder.py` 삭제 후 남은 import 정리 (`grep`으로 `car.builder` 참조 잔존 여부 확인) → 코드에는 잔존 참조 없음(본 문서 설명 텍스트 제외).
- 전체 `pytest` 실행 — 기존 63개 테스트(문구·순서 불변) + 신규 분리 테스트(names/rule_classes/selectors/service) 모두 Green, 총 78개 통과.
- `PLAN.md`/구조 문서 갱신, 최종 커밋.

### 최종 결과물

```
car/
  models.py, names.py, validation.py, selectors.py, service.py
  rules/__init__.py, rules/base.py, rules/common.py, rules/type_specific.py
cli.py, assemble.py
tests/
  test_models.py, test_names.py, test_rules.py, test_rule_classes.py,
  test_selectors.py, test_service.py, test_input_validation.py, test_cli.py
```
`car/builder.py`는 완전히 제거되었고, `cli.py`는 `CarAssemblyService`(도메인 오케스트레이션)와 `car.validation`(입력 범위 검증, UI 관심사)에만 의존한다.

### 참고 — SOLID 매핑 요약

- **SRP**: `names.py`(표시명) / `selectors.py`(상태 변경) / `service.py`(오케스트레이션) / `rules/`(규칙 판정)로 "변경 이유"가 하나씩만 남도록 분리.
- **OCP**: 신규 규칙·신규 차량 타입 추가 시 `Rule` 인스턴스만 추가, `validate()`/`CarAssemblyService` 수정 불필요.
- **LSP**: 모든 규칙이 동일한 `Rule` 인터페이스(`is_violated`, `message`)를 만족하므로 서로 치환 가능.
- **ISP**: `cli.py`는 `CarAssemblyService`라는 좁은 인터페이스 하나만 의존, 도메인 내부 모듈 구성을 몰라도 됨.
- **DIP**: 고수준 정책(`cli.py`)이 구체 구현이 아니라 서비스 추상화에 의존, 테스트 시 대체 `CarAssemblyService`/규칙 집합 주입 가능.
