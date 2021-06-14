from random import randint, choices
from string import ascii_lowercase, digits

from fastapi import FastAPI
from pymemcache.client import base

app = FastAPI()
client = base.Client(('memcached', 11211))


@app.get('/')
def home():
    return "Hello world"

def random_string(n):
    return ''.join(choices(ascii_lowercase + digits, k=n))

def random_obj(n):
    choice = randint(0, 4)
    if choice == 0:
        return randint(0, n)
    elif choice == 1:
        return random_string(n // 2)
    elif choice == 2:
        return {random_string(n // 4): random_string(n // 3)}
    elif choice == 3:
        return [i for i in range(n//2)]
    else:
        return n

def generate_complex_object(n):
    obj = []
    for i in range(n):
        sub_obj = {}
        for j in range(randint(0, n)):

            sub_obj[random_string(randint(1, 20))] = random_obj(n)
        obj.append(sub_obj)
    return obj

@app.get('/set')
def set():
    try:
        obj = generate_complex_object(100)
        client.set("obj", obj)
        return obj
    except Exception as e:
        return e.message

@app.get('/get')
def get():
    return str(client.get('obj'))
