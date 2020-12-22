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
Wirefish est un projet réalisé dans le cadre de l'UE LU3IN033-Réseaux.
Par son utilisation ancestrale, Wirefish a pour optique de ne pas remplacer Wireshark. 

## Prérequis
   * [Python 3.8+](https://www.python.org/downloads/)
   * [Urwid 2.1+](http://urwid.org/)

## Installation
Télécharcher la [Version 0.0](https://github.com/Anidwyd/wirefish/archive/v0.0.zip).

## Utilisation
Placer le fichier (format Hexdump) à analyser dans le dossier `/inputs`. Exécuter la commande :

```bash
# Selon votre installation de Python
python3 src/wirefish.py <nom_du_fichier>
python src/wirefish.py <nom_du_fichier>
py3 src/wirefish.py <nom_du_fichier>
...
```

**Commandes :**
   * Etendre / Réduire : `+ / - / CLIC GAUCHE`
   * Déplacements: `HAUT, BAS, GAUCHE, DROITE`
   * Racine / Dernier noeud ouvert: `DEBUT / FIN`
   * Haut de page / Bas de page : `PAGE HAUT / PAGE BAS`
