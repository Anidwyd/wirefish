<div align="center">
<pre>
██╗    ██╗██╗██████╗ ███████╗███████╗██╗███████╗██╗  ██╗
██║    ██║██║██╔══██╗██╔════╝██╔════╝██║██╔════╝██║  ██║
██║ █╗ ██║██║██████╔╝█████╗  █████╗  ██║███████╗███████║
██║███╗██║██║██╔══██╗██╔══╝  ██╔══╝  ██║╚════██║██╔══██║
╚███╔███╔╝██║██║  ██║███████╗██║     ██║███████║██║  ██║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
WIRESHARK MAIS EN MOINS BIEN.
</pre>
</div>

## Aperçu du projet
Wirefish est un _Analyseur de Protocole Réseau Offline_ réalisé dans le cadre du projet de l'UE "LU3IN033 Réseaux". Par son utilisation ancestrale, Wirefish a pour optique de ne pas remplacer Wireshark. 

## Prérequis
   * [Python 3.8+](https://www.python.org/downloads/)
   * [Urwid 2.1+](http://urwid.org/)

## Installation
Télécharcher et décompresser l'archive : [📚 Wirefish v0.0](https://github.com/Anidwyd/wirefish/archive/master.zip).

## Utilisation
Placer le fichier (format Hexdump) à analyser dans le dossier `/inputs`. Exécuter la commande :

```bash
# Selon votre installation de Python
python3 src/wirefish.py <nom_du_fichier>
python src/wirefish.py <nom_du_fichier>
py3 src/wirefish.py <nom_du_fichier>
...
```

Le résultat de l'analyse est affiché sous la forme d'un arbre extensible dans la console. Un fichier texte résumant l'analyse est généré dans le dossier `/outputs`.

__Commandes :__
   * Étendre / Réduire : `+ / - / CLIC GAUCHE`
   * Déplacements : `HAUT, BAS, GAUCHE, DROITE`
   * Racine / Dernier noeud visible : `DEBUT / FIN`
   * Haut de page / Bas de page : `PAGE HAUT / PAGE BAS`
   * Quitter : `Q`

## Structure de l'analyseur

Le but de l'analyseur est de décripter une trace au format Hexdump. Le resultat de l'analyse est représenté sous la forme d'un arbre. On utilisera des dictionnaires pour décrire chaque noeud : {nom du parent : (valeur du parent, fils)}.

Le programme commence par analyser la conformité du fichier donné en entrée. Ce fichier est ensuite découpé en une liste de trames, envoyée à un `Sequencer`. Chaque trame est elle-même découpée en séquences d'octets. Chaque séquence représente un protocole.
Un protocole est défini par un datagramme. Ainsi, la classe `Datagram` permet de décrire un protocole à partir d'une séquence d'octet.<br />
Un `Datagram` possède un nom, une séquence, et un dictionnaire `fields` décrivant les champs du protocole. Pour chaque champ, il précise son nom, sa taille (en bits), une fonction optionnelle pour decrire sa valeur et un dictionnaire contenant les sous-champs associés. Cette classe possède une fonction `decode()`, qui a partir de son attribut `fields` parcourt la séquence d'octets pour construire le noeud du protocole associé.<br />
Les classes `Eth`, `Ip`, `Tcp`, `Http` héritent de la classe `Datagram`. Chacune possède un attribut `fields` unique et des fonctions optionnelles pour décrire la valeur de certains champs.<br />
Enfin, une classe `Interface` construit l'interface graphique.<br />

## Auteurs
   * Jules Dubreuil - [@Anidwyd](http://github.com/anidwyd)
   * Jules Galliot - [@jugall](http://github.com/jugall)
   * Harold Kasten - [@Alkebas](https://github.com/alkebas)
