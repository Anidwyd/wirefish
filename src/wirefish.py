import os
import sys

from sequencer import Sequencer
from interface import Interface


def get_trames_list(filename):
    """ Découpe la chaine d'octets en une liste de trames.
        Retourne la liste des trames trouvées.
        Verifie la conformité du fichier. """

    with open(filename) as filehandle:
        lines = list(filter(str.strip, filehandle.readlines()))

    # Découper le fichier en une liste de trames
    trames = []
    reader = ''
    nbl = 1

    for line in lines:
        if not line.isspace():
            try:
                [offset, bytes_line] = line.split(' ', 1)
                bytes_line = " ".join(bytes_line.splitlines()).lower()

                # Tester l'encodage de l'offset et des octets
                if len(offset) < 2:
                    raise Exception('Offset mal codé : ' + offset)

                for byte in list(filter(None, bytes_line.split(' '))):
                    if int(byte, 16) > 255:
                        raise Exception('Octet mal codé : ' + byte)

                # Détecter une nouvelle trame
                if int(offset, 16) == 0 and reader:
                    trames.append(reader)
                    reader = ''

                # Si aucun soucis, ajouter la ligne
                reader += bytes_line.replace(' ', '')

            except Exception as e:
                print("Ligne " + str(nbl) + " ignorée : ")
                print(e)
                sys.exit()

        nbl += 1
    
    trames.append(reader)

    return trames
        

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


def get_text_output(dico, i=0):
    """ Genere le résultat texte de l'analyse à partir du
        dictionnaire de la trace. """

    out = ''
    for field_name in dico:
        (val, children) = dico[field_name]
        out += '\t'*i + field_name + val + '\n'
        if children:
            out += get_text_output(children, i+1)
    return out


def main():
    # Test sur l'utilisation du programme
    if len(sys.argv) != 2:
        print("Utilisation : python3 wirefish.py <nom du fichier>")
        exit(1)

    # Récuperer les fichiers
    dirname = os.path.dirname(__file__)

    inputname = sys.argv[1]
    inputpath = os.path.join(dirname, '../inputs/' + inputname)

    outputname = sys.argv[1].replace('/', '_') + '.txt'
    outputpath = os.path.join(dirname, '../outputs/analyse_' + outputname)

    if not os.path.isfile(inputpath):
        print("{} n'existe pas ".format(inputpath))
        exit(1)

    # Construction du dictionnaire de la trace.
    trace_dict = Sequencer(get_trames_list(inputpath)).sequence()

    # A partir de trace_dict, générer le fichier texte résumant l'analyse du fichier.
    with open(outputpath, 'w') as f:
        f.write('Analyse du fichier : ' + sys.argv[1] + '\n\n' + get_text_output(trace_dict))

    # Construction de l'arbe de la trace à partir de trace_dict
    retval = {"name": "Fichier analysé : " + inputname, "children":[]}
    tree = get_trace_tree(trace_dict, retval)

    # Afficher l'interface
    Interface(tree).main()


if __name__ == "__main__":
    main()