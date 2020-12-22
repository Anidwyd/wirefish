from math import ceil
import util


class Datagram:
    """ Classe définissant un datagramme. """

    def __init__(self, sequence, name):
        """ Un datagramme est une structure décrivant un protocole.
            On construit un datagramme a partir d'une sequence d'octets. """

        self.name = name
        self.sequence = sequence

        # Dictionnaire décrivant les champs du protocole.
        # Pour chaque champs, précise son nom, sa taille (en bits), une fonction
        # optionnelle pour decrire sa valeur, un dictionnaire contenant ses sous-champs.
        self.fields = dict()


    def __decode__(self, fields=None, sequence=None, seqType='hex'):
        """ A partir du dictionnaire fields, parcourt la sequence d'octets pour
            constuitre le noeud du protocole associé. """

        if not self.fields: return ''
        if not sequence: sequence = self.sequence
        if not fields: fields = self.fields

        cursor = 0
        seq_size = len(sequence)
        node = dict()

        # Pour chaque nom de champs de le dictionnaire de champs
        for f_name in fields:
            # Recuperer les informations du champs
            (f_size, v_format, f_get_opt, f_children) = fields[f_name]
            nd_children = dict()

            # Recuperer la valeur du champs dans le sequence
            if seqType == 'hex':
                f_size = max(f_size//4, 1)   # Si sequence d'octets
            
            val = ( sequence[cursor:cursor+f_size]  if cursor+f_size < seq_size
                                                    else sequence[-f_size:] )

            # Incrementer la position du curseur dans la sequence
            cursor += f_size

            # Si le champs possède des fils, décoder la valeur (chaine de bits) du champs
            if f_children:
                # Convertir la valeur en chaine de bits
                val_to_bit = ( "{0:0"+str(ceil(f_size)*4)+"b}").format(int(val, 16) )
                nd_children = self.__decode__( f_children, val_to_bit, 'bin' )
    
            # Construire le noeud
            node[f_name + ': '] = ( util.formatRaw(val, v_format)  + (' (' + f_get_opt(val) + ')' if f_get_opt else ''), nd_children )
       
        return node


    def addNode(self, frame):
        """ Ajoute le noeud de ce protocole commme fils au noeud de la trame
            donnée en paramètre. """

        node = self.__decode__()
        if node:
            frame[self.name + ': '] = ('', node)


    def __isSet__(self, value) -> str:
        """ Renvoie "Set" si la valeur du bit du champs est de 1,
            "Not Set" sinon. """

        if not (value.__contains__('0') or value.__contains__('1')):
            return 'Invalid Value'
        if (int(value, 2) > 0):
            return 'Set'
        return 'Not set'


    def __headerLen__(self, value) -> str:
        """ Renvoie la taille en octets d'une entête. """

        return str(int(value, 16)*4) + ' bytes'




class Eth(Datagram):
    """ Classe définissant une en-tête Ethernet.
        Elle herite de la classe Datagram. """

    def __init__(self, sequence):
        super().__init__(sequence, 'Ethernet II')

        self.fields = {
            'Destination': (48, 'mac', None, {}),
            'Source': (48, 'mac', None, {}),
            'Type': (16, 'hex', self.__getType__, {}),
        }

    
    def __getType__(self, value) -> str:
        """ Retourne le type de la trame Ethernet. """

        return {
            '0800': 'IPv4',
            '0806': 'ARP',
            '86DD': 'IPv6'
        }.get(value, 'Unknown')




class Ip(Datagram):
    """ Classe définissant une en-tête IP.
        Elle herite de la classe Datagram. """

    def __init__(self, sequence, ihl):

        super().__init__(sequence, 'Internet Protocol (IP)')
        
        self.ihl = ihl

        self.fields = {
            'Version': (4, 'hex', self.__getVers__, {}),
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
            'Protocol': (8, 'hex', self.__getProtocol__, {}),
            'Header Checksum': (16, 'hex', None, {}),
            'Source IP Address': (32, 'ip4', None, {}),
            'Destination IP Address': (32, 'ip4', None, {}),
        }

        if self.ihl > 5:
            self.fields['Options'] = ((self.ihl-5)*4, 'hex', None, {})


    def __getVers__(self, value):
        """ Retourne la version du protocole IP. """

        return {
            '0': 'Reserved',
            '4': 'IPv4',
            '6': 'IPv6',
            '10': 'Reserved',
        }.get(value, 'Unassigned')


    def __getProtocol__(self, value) -> str:
        """ Retourne le type de Data qui se trouve derrière l’entête IP. """

        return {
            '01': 'ICMP',
            '02': 'IGMP',
            '06': 'TCP',
            '17': 'UDP',
        }.get(value, 'Unknown')




class Tcp(Datagram):
    """ Classe définissant une en-tête TCP.
        Elle herite de la classe Datagram. """

    last_port = None

    syn_raw = None
    ack_raw = None

    def __init__(self, sequence, thl, src):
    
        super().__init__(sequence, 'Transmission Control Protocol (TCP)')

        self.thl = thl
        self.src = src

        self.fields = {
            'Source Port': (16, 'dec', None, {}),
            'Destination Port': (16, 'dec', None, {}),
            'Sequence Number': (32, 'dec', self.__getSynRel__, {}),
            'Acknowledgment Number': (32, 'dec', self.__getAckRel__, {}),
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


    def __isSame__(self):
        """ Renvoie True si on est toujours sur la meme machine,
            False sinon. """

        if Tcp.last_port != self.src:
            Tcp.last_port = self.src
            return False
        return True


    def __getSynRel__(self, value):
        """ Retourne le numéro du paquet.  """

        # Si c'est une autre machine qui envoie, on inverse SYN et ACK
        if not self.__isSame__():
            Tcp.ack_raw, Tcp.syn_raw = Tcp.syn_raw, Tcp.ack_raw
        value = int(value, 16)
        if not Tcp.syn_raw:
            Tcp.syn_raw = value
        return 'relative: ' + str(abs(value - Tcp.syn_raw))


    def __getAckRel__(self, value):
        """ Retourne le numéro du prochain paquet attendu.  """

        value = int(value, 16)
        if not Tcp.ack_raw:
            Tcp.ack_raw = value
        return 'relative: ' + str(abs(value - Tcp.ack_raw))



class Http(Datagram):
    
    def __init__(self, sequence):

        super().__init__(sequence, 'Hypertext Transfer Protocol (HTTP)')


    # Définition d'une methode __decode__ adaptée au protocole HTTP    
    def __decode__(self):
        node = dict()

        # Liste contenant la ligne de requete/réponse, puis les lignes d'en-têtes.
        # Les lignes de l'en-tête sont séparées par un retour chariot et d’un saut
        # de ligne (0x0d0a en ascii).
        head = list(filter(None, self.sequence.split('0d0a')))

        for line in head:
            # Les champs d’entête sont séparés par un espace (0x20).
            # out += '\t' + " ".join([util.hexToStr(val) for val in line.split('20')]) + '\n'
            tmp = [util.hexToStr(val) for val in line.split('20')]
            node[tmp[0] + ' '] = (" ".join(tmp[1:]), {})

        return node