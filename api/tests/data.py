from api.extensions import fake

user_one = {
    "username": fake.user_name(),
    "email": fake.email(),
    "password": fake.password(),
}

user_two = {
    "username": fake.user_name(),
    "email": fake.email(),
    "password": fake.password(),
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
