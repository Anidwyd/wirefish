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
   
## Auteurs
   * Jules Dubreuil - [@Anidwyd](http://github.com/anidwyd)
   * Jules Galliot - [@jugal](http://github.com/jugal)
   * Harold Kasten - [@Alkebas](https://github.com/alkebas)
