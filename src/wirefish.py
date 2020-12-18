from util import colorText
from sequencer import Sequencer
 
def main():
    # f = open("../data/ascii/text.txt","r")
    # print("".join(f.readlines()))

    s = Sequencer('tests/message_answer')
    s.__sequence__()

if __name__ == "__main__":
    main()