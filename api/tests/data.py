from random import choice, uniform
from api.extensions import fake

user_one = {
    "username": fake.user_name(),
    "email": fake.email(),
    "password": "!XvDzRasj9",
}

user_two = {
    "username": fake.user_name(),
    "email": fake.email(),
    "password": "!XvDzRasj9",
}

customer_one = {
    "company": fake.company(),
    "email": fake.email(),
    "name": fake.name(),
    "telephone": fake.msisdn()[3:],
}

customer_two = {
    "company": fake.company(),
    "email": fake.email(),
    "name": fake.name(),
    "telephone": fake.msisdn()[3:],
}

vehicle_one = {
    "name": fake.first_name_nonbinary(),
    "cost_per_day": round(uniform(300, 700), 2),
    "penalty_per_day": round(uniform(100, 200), 2),
    "vehicle_type": choice(["saloon", "bus", "motor_cycle", "bicycle"]),
    "rented": False,
}

vehicle_two = {
    "name": fake.first_name_nonbinary(),
    "cost_per_day": round(uniform(300, 700), 2),
    "penalty_per_day": round(uniform(100, 200), 2),
    "vehicle_type": choice(["saloon", "bus", "motor_cycle", "bicycle"]),
    "rented": False,
}
