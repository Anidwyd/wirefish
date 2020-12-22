import os
import re

from datagram import Eth, Ip, Tcp, Http

class Sequencer:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            print("{} does not exist ".format(filename))
            exit(1)
        self.filename = filename

    def sequence(self):
        """ Découpe la chaine d'octets en une liste de trames.
            Chaque trame est ensuite elle-même découpée en séquences.
            Chaque séquence représente un protocole. """

        with open(self.filename) as filehandle:
            lines = filter(str.strip, filehandle.readlines())

        # Découper le fichier en une liste de trames
        trames = []
        reader = ''
        for line in lines:
            if not line.isspace():
                if line[:4] == '0000' and reader:
                    trames.append(reader)
                    reader = ''
                # Retirer l'offset et le retour a la ligne
                reader += line.replace(' ', '')[4:]
                reader = " ".join(reader.splitlines())
        
        trames.append(reader)

        # Construction du dictionnaire de la trace
        trace_tree = dict()

        # Découper chaque trames en sections (une section = un protocol)
        for i in range(len(trames)):
            t = trames[i]
            tsize = len(t)

            # Indices de fin de chaque sequence  + calcul de l'ihl et du thl
            eoEth = 14 * 2                  # enf_of_eth = 14 (bytes) * 2
            ihl = int(t[eoEth+1], 16)
            eoIp = eoEth + ihl * 4 * 2      # end_of_ip  = (IHL * 4) * 2
            thl = int(t[eoIp+24], 16)
            src = int(t[eoIp:eoIp+4], 16)
            eoTcp = eoIp + thl * 4 * 2      # end_of_tcp = (THL * 4) * 2
            
            # Decoupage de la trame en séquence d'octets
            ether_seq = t[:eoEth]
            ip_seq = t[eoEth:eoIp]
            tcp_seq = t[eoIp:eoTcp]
            http_seq = t[eoTcp:]

            # Construction du noeud de la trame
            frame_node = dict()
            Eth(ether_seq).addNode(frame_node),
            Ip(ip_seq, ihl).addNode(frame_node)
            Tcp(tcp_seq, thl, src).addNode(frame_node)
            Http(http_seq).addNode(frame_node)

            # Ajout du noeud dans l'arbre de la trace
            trace_tree['Frame ' + str(i+1) + ': '] = ( str(tsize//2) + ' octets ('+ str(tsize*4) + ' bits)', frame_node)

        return trace_tree


    def isValid(self):
        # TODO: vérifier l'entrée
        # - Chaque octet est codé par deux chiffres hexadécimaux.
        # - Chaque octet est délimité par un espace.
        # - Chaque ligne commence par l’offset du premier octet situé à la suite sur la même
        # ligne. L’offset décrit la positon de cet octet dans la trace.
        # - Chaque nouvelle trame commence avec un offset de 0 et l’offset est séparé d’un
        # espace des octets capturés situés à la suite.
        # - L’offset est codé sur au moins un octet donné en valeur hexadécimale (deux
        # chiffres hexadécimaux).
        # - Les caractères hexadécimaux peuvent être des majuscules ou minuscules.
        # - Il n’y a pas de limite concernant la longueur ou le nombre d’octets présents sur
        # chaque ligne.
        # - Si des valeurs textuelles sont données en fin de ligne, elles doivent être ignorées,
        # y compris si ces valeurs sont des chiffres hexadécimaux.
        # - Les lignes de texte situées entre les traces ou entrelacées entre les lignes
        # d’octets capturés doivent être ignorées.
        # - Les lignes d’octets qui ne débutent pas un offset valide doivent être ignorées.
        # - Toute ligne incomplète doit être identifiée et soulever une erreur indiquant la
        # position de la ligne en erreur. 
        pass