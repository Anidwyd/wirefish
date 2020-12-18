from datagram import Eth, Ip, Tcp, Http
import os

class Sequencer:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            print("{} does not exist ".format(filename))
            exit(1)
        self.filename = filename

    def __sequence__(self):
        with open(self.filename) as filehandle:
            lines = filter(str.strip, filehandle.readlines())

        reader = ''
        trames = []

        # Découper le fichier en une liste de trames
        for line in lines:
            if not line.isspace():
                if line[:4] == '0000' and reader:
                    trames.append(reader)
                    reader = ''
                # Retirer l'offset et le retour a la ligne
                reader += line.replace(' ', '')[4:]
                reader = " ".join(reader.splitlines())
        
        trames.append(reader)

        # Pour chaque trame
        for i in range(len(trames)):
            t = trames[i]
            tsize = len(t)
            print('\nTrame ' + str(i+1) + ': ' + str(tsize//2) + ' octets ('+ str(tsize*4) + ' bits)')
            
            # Indices de fin de chaque section,
            # Calcul de l'ihl et du thl
            eoEth = 14 * 2                  # enf_of_eth = 14 (bytes) * 2
            ihl = int(t[eoEth+1], 16)
            eoIp = eoEth + ihl * 4 * 2      # end_of_ip  = (IHL * 4) * 2
            thl = int(t[eoIp+24], 16)
            eoTcp = eoIp + thl * 4 * 2      # end_of_tcp = (THL * 4) * 2
            
            # Decoupage de la trame en séquence d'octets
            ether_seq = t[:eoEth]
            ip_seq = t[eoEth:eoIp]
            tcp_seq = t[eoIp:eoTcp]
            http_seq = t[eoTcp:]

            # Affichage du decodage
            print( Eth(ether_seq).getOutput() )
            print( Ip(ip_seq, ihl).getOutput() )
            print( Tcp(tcp_seq, thl).getOutput() )
            print( Http(http_seq).getOutput() )