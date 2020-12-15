from math import ceil
from values import *

def ethernet(seq: str) -> str:
    """
    Analyse le protocole Ethernet de la trame
    """
    if len(seq) < 14:
        print('Erreur: trame mal formatée')
        exit(1)

    ethernet_fields = {
    #   field_name: (b_size: int, val_format: str, get_opt: func, {sons})
        'Destination': (48, 'mac', None, {}),
        'Source': (48, 'mac', None, {}),
        'Type': (16, 'hex', None, {}),
    }

    return 'Ethernet II:\n' + build_fields(ethernet_fields, seq)


def ip4(seq: str) -> str:
    """
    Analyse le protocole IP de la trame
    """

    ip_fields = {
    #   f_name: (f_size: int, val_format: str, get_opt: func, {sons})
        'Version': (4, 'hex', None, {}),
        'Header Length': (4, 'hex', None, {}),
        'Type of Service': (8, 'hex', None, {}),
        'Total Length': (16, 'hex', None, {}),
        'Identifier': (16, 'hex', None, {}),
        'Flags': (3, '', None, {
            'Reserved bits': (1, 'bin', None, {}),
            'Don\'t fragment': (1, 'bin', None, {}),
            'More fragments': (1, 'bin', None, {}),
        }),
        'Fragment Offset': (13, 'hex', None, {}),
        'Time to Live': (8, 'hex', None, {}),
        'Protocol': (8, 'hex', None, {}),
        'Header Checksum': (16, 'hex', None, {}),
        'Source IP Address': (32, 'ip4', None, {}),
        'Destination IP Address': (32, 'ip4', None, {}),
    }

    opt_size = (len(seq.replace(' ', ''))//2 - 20) * 8
    if opt_size > 0:
        ip_fields['Options'] = (opt_size, 'hex', None, {})

    return 'Internet Protocol (IP):\n' + build_fields(ip_fields, seq)


def tcp(seq: str) -> str:
    """
    Analyse le protocole TCP de la trame
    """

    tcp_fields = {
    #   f_name: (b_size: int, val_format: str, get_opt: func, {sons})
        'Source Port': (16, 'hex', None, {}),
        'Destination Port': (16, 'hex', None, {}),
        'Sequence Number': (32, 'hex', None, {}),
        'Acknowledgment Number': (32, 'hex', None, {}),
        'Header Length': (4, 'hex', None, {}),
        'Flags': (12, '', None, {
            'Reserved': (6, 'bin', None, {}),
            'Urgent': (1, 'bin', None, {}),
            'Acknowledgment': (1, 'bin', None, {}),
            'Push': (1, 'bin', None, {}),
            'Reset': (1, 'bin', None, {}),
            'Syn': (1, 'bin', None, {}),
            'Fin': (1, 'bin', None, {}),
        }),
        'Window': (16, 'hex', None, {}),
        'Checksum': (16, 'hex', None, {}),
        'Urgent Pointer': (16, 'hex', None, {}),
    }

    opt_size = (len(seq.replace(' ', ''))//2 - 20) * 8
    if opt_size > 0:
        tcp_fields['Options'] = (opt_size, 'hex', None, {})

    return 'Transmission Control Protocol (TCP):\n' + build_fields(tcp_fields, seq)


def http(seq: str) -> str:
    """
    Analyse le protocole HTTP de la trame
    """
    pass


def build_fields(tr_fields: dict(), seq: str, indent=1, cursor=0) -> str:
    out_str = ''    # decoder

    # for each field's name in the trace's fields
    for f_name in tr_fields:
        (f_size, v_format, get_opt, sons) = tr_fields[f_name]
        val, size = get_value(seq, cursor, f_size, v_format)
        out_str += '\t'*indent + f_name + ': ' + format_val(val, v_format) + '\n'
        if sons:
            val_to_bit = ("{0:0"+str(ceil(f_size/4)*4)+"b}").format(int(val, 16))
            out_str += build_fields(sons, val_to_bit, indent+1, 0)
        cursor += size
 
    return out_str