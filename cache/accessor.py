import redis

def get_redis_connection()->redis.Redis:
    return redis.Redis(host='localhost', port=6379, db=0)

def set_pomodoro_count():
    redis = get_redis_connection()
    # redis.set('pomodoro_count', 1)
    # redis.set('pomodoro_count', 2)
    redis.set('pomodoro_count', 3, ex = 10)
    redis.json().set("bike", "$", '"Hyperion"')
    redis.hset(
        "bike:4",
        mapping={
            "model": "Deimos",
            "brand": "Ergonom",
            "type": "Enduro bikes",
            "price": 4972
        }
    )




if __name__ == '__main__':
    set_pomodoro_count()