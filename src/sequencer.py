from datagram import Eth, Ip, Tcp, Http
import os

class Sequencer:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            print("{} does not exist ".format(filename))
            exit(1)
        self.filename = filename

    def __sequence__(self):
        res = ''

        with open(self.filename) as filehandle:
            lines = filter(str.strip, filehandle.readlines())
            res += 'Analyse du fichier : ' + filehandle.name + '\n' 

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

        # Pour chaque trame
        for i in range(len(trames)):
            t = trames[i]
            tsize = len(t)
            res += ('\nTrame ' + str(i+1) + ': ' + str(tsize//2) +
                    ' octets ('+ str(tsize*4) + ' bits)\n')
            
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
            res += (Eth(ether_seq).getOutput() +
                    Ip(ip_seq, ihl).getOutput() +
                    Tcp(tcp_seq, thl).getOutput() +
                    Http(http_seq).getOutput())

        with open('res.txt', 'w') as out:
            out.write(res)
        print(res)