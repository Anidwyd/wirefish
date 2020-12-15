def get_value(seq: str, cursor: int, f_size: int, v_format: str) -> (str, int):
    # TODO: gerer la valeur des fils
    size = max(f_size//4, 1) if v_format != 'bin' else f_size    # size of the field in the seq
    eo_field = cursor + size    # end of the field index
    val = seq[cursor:eo_field] if eo_field < len(seq) else seq[-size:]

    return val, size


def format_val(val: str, v_format: str) -> str:
    """
    Retourne la valeur donnée dans le format choisi.
    """
    formats = {
        'bin':  val,
        'hex':  '0x' + val,
        'mac':  ':'.join(["".join(x) for x in zip(*[iter(val)]*2)]),
        'ip4':  '.'.join([str(int(x, 16)) for x in [''.join(x) for x in zip(*[iter(val)]*2)]]),
    }

    return formats.get(v_format, '')