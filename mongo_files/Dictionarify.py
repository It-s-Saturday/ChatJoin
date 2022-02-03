def dictionarify(key, value, key1='', value1='', key2='', value2='', key3='', value3=''):
    # key, value
    # key1, value1
    # key2, value2
    # key3, value3
    d = {key, value} or {}
    if key and value:
        if key1 and value1:
            d = {key: value, key1: value1}
            if key2 and value2:
                d = {key: value, key1: value1, key2: value2}
                if key3 and value3:
                    d = {key: value, key1: value1, key2: value2, key3: value3}
    return d
