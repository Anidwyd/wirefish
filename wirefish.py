def analyse_frame(frame_src: str) -> int:
    """
    Analyse la trame
    """
    # frame = open(frame_src, 'r')
    # res = open('./result.txt', 'w')

    buffer = ""
    print(analyse_ethernet("00 cb 51 d0 aa 8c c8 d3 ff 44 98 38 08 00"))
    print(analyse_ip("45 00 02 08 dc 10 40 00 80 06 05 b2 c0 a8 01 39 68 13 ed"))
    analyse_tcp("dd 0a 00 50 9e 5a 0e db c1 2c 15 ee 50 18 04 04 b7 15 00 00")
    # analyse_http("00 cb 51 d0 aa 8c c8 d3 ff 44 98 38 08 00")

    return 1


def analyse_ethernet(buffer: str) -> str:
    """
    Analyse le protocole Ethernet de la trame
    """
    if len(buffer) < 41:
        print('Erreur: trame mal formatée')
        exit(1)

    return ('\n***Champ Ethernet***' +
            get_field('Destination', buffer[:16].replace(' ', ':'), isHex=False) +
            get_field('Source', buffer[18:34].replace(' ', ':'), isHex=False) +
            get_field('Type', buffer[-5:], opt="IPv4"))

def analyse_ip(buffer: str) -> str:
    """
    Analyse le protocole IP de la trame
    """
    ip_ver = buffer[0]
    h_len = buffer[1]
    t_len = buffer[6:11]
    ident = buffer[12:17]
    
    return ("\n*** Champ IP ***" +
            get_field('Version', ip_ver, opt=ip_ver) +
            get_field('Header Length', h_len, opt=str(int(h_len)*4) + ' bytes',) +
            get_field('Differentiated Services Field') +
                get_field('Differential Services Codepoint', buffer[3], 2) +
                get_field('Explicit Congestion Notification', buffer[4], 2) +
            get_field('Total Length', t_len, opt=ip_ver) +
            get_field('Identification', ident, opt=str(int(h_len)*4) + ' bytes',) +
            get_field('Flags', buffer[0]) +
                get_field('Reserved bit', buffer[0], 2) +
                get_field('Don\'t fragment', buffer[0], 2) +
                get_field('More fragments', buffer[0], 2) +
            get_field('Fragment Offset', buffer[0]) +
            get_field('Time to Live', buffer[0]) +
            get_field('Protocol', buffer[0]) +
            get_field('Header checksum', buffer[0]) +
            get_field('Source Address', buffer[0]) +
            get_field('Destination Address', buffer[0]))


def analyse_tcp(buffer: str) -> str:
    """
    Analyse le protocole TCP de la trame
    """
    pass


def analyse_http(buffer: str) -> str:
    """
    Analyse le protocole HTTP de la trame
    """
    pass


### UTIL ###

def get_field(field_name, value='', indent=1, isHex=True, opt='') -> str:
    out_str = ('\n'+'\t'*indent + field_name + ': ' +
                ('0x' + value.replace(' ', '') if isHex else value))
    return out_str if (opt == '') else out_str + ' (' + opt + ')'

############


def main():
    frame_src = './trame_tcp'
    # print("Wirefish : Wireshark but worse.\n\n")
    if analyse_frame(""):
        # print("\n\nAnalyse terminée avec succès.")
        return 0
    # print("Analyse terminée avec erreur.")
    return 1

if __name__ == "__main__":
    main()