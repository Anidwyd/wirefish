import os
import sys

from sequencer import Sequencer
from interface import Interface

def get_trace_tree(trace, retval):
    """ Genere l'arbre a partir du dictionnaire de la trace. """

    i = 0
    for field_name in trace:
        (val, children) = trace[field_name]
        retval['children'].append({"name": field_name + val})
        if children:
            retval['children'][i]['children'] = []
            get_trace_tree(children, retval['children'][i])
        i += 1
    return retval


def get_text_output(trace, i=0):
    """ Genere le résultat texte de l'analyse à partir du
        dictionnaire de la trace. """

    out = ''
    for field_name in trace:
        (val, children) = trace[field_name]
        out += '\t'*i + field_name + val + '\n'
        if children:
            out += get_text_output(children, i+1)
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage : python3 wirefish.py <fichier raw hex>")
        exit(1)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, sys.argv[1])

    trace_dict = Sequencer(filename).sequence()

    with open('../res.txt', 'w') as f:
        f.write('Analyse du fichier : ' + f.name + '\n\n' + get_text_output(trace_dict))

    retval = {"name": "Trames reconnues:", "children":[]}
    tree = get_trace_tree(trace_dict, retval)

    Interface(tree).main()


if __name__ == "__main__":
    main()