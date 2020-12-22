def formatRaw(val: str, v_format: str) -> str:
    """ Retourne la valeur (raw) dans le format choisi. """
    formats = {
        'bin':  val,
        'hex':  '0x' + val,
        'dec':  str(int(val, 16)),
        'mac':  ':'.join(["".join(x) for x in zip(*[iter(val)]*2)]),
        'ip4':  '.'.join([str(int(x, 16)) for x in [''.join(x) for x in zip(*[iter(val)]*2)]]),
    }

    return formats.get(v_format, '')


def hexToDec(val) -> str:
    """ Retourne la valeur hexadécimal en décimal. """

    return formatRaw(val, 'dec')


def hexToStr(val) -> str:
    """ Decode une valeur hexadécimal. """

    return bytes.fromhex(val).decode('utf-8')