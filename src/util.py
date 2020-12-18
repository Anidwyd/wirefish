import os

COLORS = {
    'black': '\u001b[30m',
    'red': '\u001b[31m',
    'green': '\u001b[32m',
    'yellow': '\u001b[33m',
    'blue': '\u001b[34m',
    'magenta': '\u001b[35m',
    'cyan': '\u001b[36m',
    'white': '\u001b[37m',
    'bblack': '\u001b[30;1m',
    'bred': '\u001b[31;1m',
    'bgreen': '\u001b[32;1m',
    'byellow': '\u001b[33;1m',
    'bblue': '\u001b[34;1m',
    'bmagenta': '\u001b[35;1m',
    'bcyan': '\u001b[36;1m',
    'bwhite': '\u001b[37;1m',
    'reset': '\u001b[0m',
}

def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text
    

def formatRaw(val: str, v_format: str) -> str:
    """
    Retourne la valeur raw dans le format choisi.
    """
    formats = {
        'bin':  val,
        'hex':  '0x' + val,
        'dec':  str(int(val, 16)),
        'mac':  ':'.join(["".join(x) for x in zip(*[iter(val)]*2)]),
        'ip4':  '.'.join([str(int(x, 16)) for x in [''.join(x) for x in zip(*[iter(val)]*2)]]),
    }

    return formats.get(v_format, '')


def hexToDec(val) -> str:
    return formatRaw(val, 'dec')
