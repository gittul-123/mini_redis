from redis import Redis


redis = Redis()

while True:
    command = input("mini-redis> ")

    if command.lower() == "exit" or command.lower() == "quit":
        break

    parts = command.split()

    if parts[0].upper() == "SET":
        redis.set(parts[1], parts[2])
        print("OK")

    elif parts[0].upper() == "GET":
        result = redis.get(parts[1])
        print(result)

    elif parts[0].upper() == "DEL":
        result = redis.delete(parts[1])
        print(result)

    elif parts[0].upper() == "KEYS":
        result = redis.keys()
        print(result)

    elif parts[0].upper() == "EXISTS":
        result = redis.exists(parts[1])
        print(result)

    elif parts[0].upper() == "DBSIZE":
        result = redis.dbsize()
        print(result)

    elif parts[0].upper() == "EXPIRE":
        result = redis.expire(parts[1], int(parts[2]))
        print(result)

    elif parts[0].upper() == "TTL":
        result = redis.ttl(parts[1])
        print(result)

    elif parts[0].upper() == "CONFIG":
        if parts[1].upper() == "SET" and parts[2].lower() == "maxmemory":
            result = redis.config(parts[3])
            print(result)

    elif parts[0].upper() == "INFO":
        if parts[1].lower() == "memory":
            result = redis.info()
            print(result)    