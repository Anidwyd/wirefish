import os
import sys

from datagram import Eth, Ip, Tcp, Http

class Sequencer:
    def __init__(self, trames):
        self.trames = trames

    def sequence(self):
        """ Chaque trame est ensuite elle-même découpée en séquences.
            Chaque séquence représente un protocole. """

        # Construction du dictionnaire de la trace
        trace_tree = dict()

        # Découper chaque trames en sections (une section = un protocol)
        for i in range(len(self.trames)):
            t = self.trames[i]
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
