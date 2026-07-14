from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CarType(Enum):
    SEDAN = 1
    SUV = 2
    TRUCK = 3


class Engine(Enum):
    GM = 1
    TOYOTA = 2
    WIA = 3
    BROKEN = 4


class Brake(Enum):
    MANDO = 1
    CONTINENTAL = 2
    BOSCH = 3


class Steering(Enum):
    BOSCH = 1
    MOBIS = 2


class Step(Enum):
    CAR_TYPE = 0
    ENGINE = 1
    BRAKE = 2
    STEERING = 3
    FINAL = 4


@dataclass
class Car:
    car_type: Optional[CarType] = None
    engine: Optional[Engine] = None
    brake: Optional[Brake] = None
    steering: Optional[Steering] = None
