import trbuilder

def decoder(frame_src: str) -> int:
    """
    Analyse la trame
    """
    # frame = open(frame_src, 'r')
    # res = open('./result.txt', 'w')

    buffer = ""
    out = ""
    print(trbuilder.ethernet("00cb51d0aa8cc8d3ff4498380800"))
    print(trbuilder.ip4("45000208dc104000800605b2c0a801396813ed38"))
    print(trbuilder.tcp("dd0a00509e5a0edbc12c15ee50180404b7150000"))
    # analyse_http("00 cb 51 d0 aa 8c c8 d3 ff 44 98 38 08 00")

    return 1


def main():
    frame_src = './trame_tcp'
    # print("Wirefish : Wireshark but worse.\n\n")
    if decoder(''):
        # print("\n\nAnalyse terminée avec succès.")
        return 0
    # print("Analyse terminée avec erreur.")
    return 1

if __name__ == "__main__":
    main()