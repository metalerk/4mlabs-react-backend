def recursive_keyval(obj, prefix=''):
    keyval = dict()
    if prefix: prefix += '.'

    for item in obj.items():
        if type(item[1]) == dict:
            keyval.update(recursive_keyval(item[1], prefix=prefix+str(item[0])))
        elif type(item[1]) == list:
            for x in item[1]:
                keyval.update(recursive_keyval(x, prefix=prefix+str(item[0])))
        else:
            keyval['{}{}'.format(prefix, item[0])] = item[1]
    
    return keyval