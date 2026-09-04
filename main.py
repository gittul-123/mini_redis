from redis import Redis


redis = Redis()

while True:
    command = input("mini-redis> ")

    if command.lower() == "exit" or command.lower() == "quit":
        break

    parts = command.split()

    if len(parts) == 0:
        continue

    cmd = parts[0].upper()

    if cmd == "SET":
        if len(parts) != 3:
            print("(error) ERR wrong number of arguments for 'SET' command")
        else:
            result = redis.set(parts[1], parts[2])

            if result == "(error) OOM":
                print(result)
            else:
                print("OK")

    elif cmd == "GET":
        
        if len(parts) != 2:
            print("(error) ERR wrong number of arguments for 'GET' command")
        else:
            result = redis.get(parts[1])

            if result is None:
                print("(nil)")
            else:
                print(result)

    elif cmd == "DEL":
        if len(parts) != 2:
            print("(error) ERR wrong number of arguments for 'DEL' command")
        else:
            result = redis.delete(parts[1])
            print(f"(integer) {result}")

    elif cmd == "KEYS":
        if len(parts) != 1:
            print("(error) ERR wrong number of arguments for 'KEYS' command")
        else:
            result = redis.keys()
            print(result)

    elif cmd == "EXISTS":
        if len(parts) != 2:
            print("(error) ERR wrong number of arguments for 'EXISTS' command")
        else:
            result = redis.exists(parts[1])
            print(f"(integer) {result}")

    elif cmd == "DBSIZE":
        if len(parts) != 1:
            print("(error) ERR wrong number of arguments for 'DBSIZE' command")
        else:
            result = redis.dbsize()
            print(f"(integer) {result}")

    elif cmd == "EXPIRE":
        if len(parts) != 3:
            print("(error) ERR wrong number of arguments for 'EXPIRE' command")
        else:
            try:
                seconds = int(parts[2])
                result = redis.expire(parts[1], seconds)
                print(result)
            except ValueError:
                print("(error) ERR value is not an integer or out of range")

    elif cmd == "TTL":
        if len(parts) != 2:
            print("(error) ERR wrong number of arguments for 'TTL' command")
        else:
            result = redis.ttl(parts[1])
            print(result)

    elif cmd == "CONFIG":
        if len(parts) != 4:
            print("(error) ERR wrong number of arguments for 'CONFIG' command")
        elif parts[1].upper() == "SET" and parts[2].lower() == "maxmemory":
            try:
                result = redis.config(parts[3])
                print(result)
            except ValueError:
                print("(error) ERR value is not an integer or out of range")
        else:
            print(f"(error) ERR unknown command '{parts[0]}'")

    elif cmd == "INFO":
        if len(parts) != 2:
            print("(error) ERR wrong number of arguments for 'INFO' command")
        elif parts[1].lower() == "memory":
            result = redis.info()
            print(result)
        else:
            print(f"(error) ERR unknown command '{parts[0]}'")

    else:
        print(f"(error) ERR unknown command '{parts[0]}'")