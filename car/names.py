from car.models import CarType, Engine, Brake, Steering

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
