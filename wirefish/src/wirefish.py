from util import colorText
from sequencer import Sequencer

def main():
    # f = open("data/fish_logo.txt","r")
    # ascii = "".join(f.readlines())
    # print(colorText(ascii))
    frame_src = './trame_tcp'
    print("Wirefish : Wireshark but worse.\n")

    s = Sequencer()
    s.sequence()

if __name__ == "__main__":
    main()