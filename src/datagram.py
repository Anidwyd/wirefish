from math import ceil
import util


class Datagram:
    """ Classe définissant un datagramme."""

    def __init__(self, sequence, name):
        self.name = name

        self.sequence = sequence
        self.seq_size = len(sequence)

        # Format du dictionnaire de champs:
        # { field_name: (field_size: int, val_format: str, get_opt: func, {sons}) }
        self.fields = dict()


    def __decode__(self, fields=None, sequence=None, indent=1, seqType='hex'):

        if not self.fields: return ''
        if not sequence: sequence = self.sequence
        if not fields: fields = self.fields

        res = ''
        cursor = 0
        seq_size = len(sequence)

        # Pour chaque nom de champs de le dictionnaire de champs
        for f_name in fields:
            # Recuperer les informations du champs
            (f_size, v_format, get_opt, sons) = fields[f_name]

            # Recuperer la valeur du champs dans le sequence
            if seqType == 'hex':
                f_size = max(f_size//4, 1)   # Si sequence d'octets
            
            val  = (sequence[cursor:cursor+f_size] if cursor+f_size < seq_size
                    else sequence[-f_size:])

            # Incrementer la position du curseur dans le sequence
            cursor += f_size

            # Mettre a jour la chaine retour
            res += '\t'*indent + f_name + ': '+ util.formatRaw(val, v_format)
            res += (' (' + get_opt(val) + ')\n' if get_opt != None else '\n')

            # Si le champs possède des fils, décoder la valeur (chaine de bits) du champs
            if sons:
                val_to_bit = ("{0:0"+str(ceil(f_size)*4)+"b}").format(int(val, 16))
                res += self.__decode__(sons, val_to_bit, indent+1, 'bin')
    
        return res


    def getOutput(self):
        return '▼ ' + self.name + ':\n' + self.__decode__()


    def __isSet__(self, value) -> str:
        if not (value.__contains__('0') or value.__contains__('1')):
            return 'Invalid Value'
        if (int(value, 2) > 0):
            return 'Set'
        return 'Not set'


    def __headerLen__(self, value) -> str:
        return str(int(value)*4) + ' bytes'




class Eth(Datagram):
    """ Classe définissant une en-tête Ethernet.
        Elle herite de la classe Datagram. """

    def __init__(self, sequence):
        super().__init__(sequence, 'Ethernet II')

        def __getType__(value) -> str:
            return {
                '0800': 'IPv4',
                '0806': 'ARP',
                '86DD': 'IPv6'
            }.get(value, 'Unknown')


        self.fields = {
            'Destination': (48, 'mac', None, {}),
            'Source': (48, 'mac', None, {}),
            'Type': (16, 'hex', __getType__, {}),
        }




class Ip(Datagram):
    """ Classe définissant une en-tête IP.
        Elle herite de la classe Datagram. """

    def __init__(self, sequence, ihl):

        super().__init__(sequence, 'Internet Protocol (IP)')
        
        self.ihl = ihl

        def __getVers__(value):
            return {
                '0': 'Reserved',
                '4': 'IPv4',
                '6': 'IPv6',
                '10': 'Reserved',
            }.get(value, 'Unassigned')


        def __getProtocol__(value) -> str:
            return {
                '01': 'ICMP',
                '02': 'IGMP',
                '06': 'TCP',
                '17': 'UDP',
            }.get(value, 'Unknown')

        self.fields = {
            'Version': (4, 'hex', __getVers__, {}),
            'Header Length': (4, 'hex', super().__headerLen__, {}),
            'Type of Service': (8, 'hex', None, {}),
            'Total Length': (16, 'hex', util.hexToDec, {}),
            'Identifier': (16, 'hex', util.hexToDec, {}),
            'Flags': (3, '', None, {
                'Reserved bits': (1, 'bin', super().__isSet__, {}),
                'Don\'t fragment': (1, 'bin', super().__isSet__, {}),
                'More fragments': (1, 'bin', super().__isSet__, {}),
            }),
            'Fragment Offset': (13, 'dec', None, {}),
            'Time to Live': (8, 'hex', util.hexToDec, {}),
            'Protocol': (8, 'hex', __getProtocol__, {}),
            'Header Checksum': (16, 'hex', None, {}),
            'Source IP Address': (32, 'ip4', None, {}),
            'Destination IP Address': (32, 'ip4', None, {}),
        }

        if self.ihl > 5:
            self.fields['Options'] = ((self.ihl-5)*4, 'hex', None, {})




class Tcp(Datagram):
    """ Classe définissant une en-tête TCP.
        Elle herite de la classe Datagram. """

    def __init__(self, sequence, thl):
    
        super().__init__(sequence, 'Transmission Control Protocol (TCP)')

        self.thl = thl

        self.fields = {
            'Source Port': (16, 'dec', None, {}),
            'Destination Port': (16, 'dec', None, {}),
            'Sequence Number': (32, 'hex', None, {}),
            'Acknowledgment Number': (32, 'hex', None, {}),
            'Header Length': (4, 'hex', super().__headerLen__, {}),
            'Flags': (12, '', None, {
                'Reserved': (6, 'bin', super().__isSet__, {}),
                'Urgent': (1, 'bin', super().__isSet__, {}),
                'Acknowledgment': (1, 'bin', super().__isSet__, {}),
                'Push': (1, 'bin', super().__isSet__, {}),
                'Reset': (1, 'bin', super().__isSet__, {}),
                'Syn': (1, 'bin', super().__isSet__, {}),
                'Fin': (1, 'bin', super().__isSet__, {}),
            }),
            'Window': (16, 'hex', util.hexToDec, {}),
            'Checksum': (16, 'hex', None, {}),
            'Urgent Pointer': (16, 'dec', None, {}),
        }

        if self.thl > 5:
            self.fields['Options'] = ((self.thl-5)*4, 'hex', None, {})




class Http(Datagram):
    
    def __init__(self, sequence):

        super().__init__(sequence, 'Hypertext Transfer Protocol (HTTP)')