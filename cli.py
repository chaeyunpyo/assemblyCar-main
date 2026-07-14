import sys
import time

from car.models import Step, CarType, Engine, Brake, Steering, Car
from car.validation import is_valid_range, ERROR_MESSAGES
from car.service import CarAssemblyService

CLEAR_SCREEN = "\033[H\033[2J"

STEP_ORDER = [Step.CAR_TYPE, Step.ENGINE, Step.BRAKE, Step.STEERING, Step.FINAL]

CAR_TYPE_BY_ANSWER = {1: CarType.SEDAN, 2: CarType.SUV, 3: CarType.TRUCK}
ENGINE_BY_ANSWER = {1: Engine.GM, 2: Engine.TOYOTA, 3: Engine.WIA, 4: Engine.BROKEN}
BRAKE_BY_ANSWER = {1: Brake.MANDO, 2: Brake.CONTINENTAL, 3: Brake.BOSCH}
STEERING_BY_ANSWER = {1: Steering.BOSCH, 2: Steering.MOBIS}


def delay(ms):
    time.sleep(ms / 1000.0)


def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def show_menu(step):
    clear()
    if step == Step.CAR_TYPE:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
        print("1. Sedan")
        print("2. SUV")
        print("3. Truck")
    elif step == Step.ENGINE:
        print("어떤 엔진을 탑재할까요?")
        print("0. 뒤로가기")
        print("1. GM")
        print("2. TOYOTA")
        print("3. WIA")
        print("4. 고장난 엔진")
    elif step == Step.BRAKE:
        print("어떤 제동장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. MANDO")
        print("2. CONTINENTAL")
        print("3. BOSCH")
    elif step == Step.STEERING:
        print("어떤 조향장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. BOSCH")
        print("2. MOBIS")
    elif step == Step.FINAL:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")
    print("===============================")


def main():
    service = CarAssemblyService()
    car = Car()
    step_index = 0

    while True:
        step = STEP_ORDER[step_index]
        show_menu(step)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not is_valid_range(step, ans):
            print(ERROR_MESSAGES[step])
            delay(800)
            continue

        if ans == 0:
            if step == Step.FINAL:
                step_index = 0
            elif step_index > 0:
                step_index -= 1
            continue

        if step == Step.CAR_TYPE:
            print(service.select_car_type(car, CAR_TYPE_BY_ANSWER[ans]))
            delay(800)
            step_index = 1
        elif step == Step.ENGINE:
            print(service.select_engine(car, ENGINE_BY_ANSWER[ans]))
            delay(800)
            step_index = 2
        elif step == Step.BRAKE:
            print(service.select_brake(car, BRAKE_BY_ANSWER[ans]))
            delay(800)
            step_index = 3
        elif step == Step.STEERING:
            print(service.select_steering(car, STEERING_BY_ANSWER[ans]))
            delay(800)
            step_index = 4
        elif step == Step.FINAL:
            if ans == 1:
                for line in service.run(car):
                    print(line)
                delay(2000)
            elif ans == 2:
                print("Test...")
                delay(1500)
                print(service.test(car))
                delay(2000)


if __name__ == "__main__":
    main()
