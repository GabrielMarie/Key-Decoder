# Générateur de calques

Génère un calque PNG transparent avec des lignes horizontales à partir d’un fichier JSON. La configuration fournie correspond aux hauteurs Kwikset.

Ce guide concerne la version française : `generer_calque.py` et le fichier `kwikset.json` contenant les clés en français.

## Prérequis

Python et la bibliothèque Pillow. Pour installer ou mettre à jour Pillow :

```bash
python -m pip install --upgrade Pillow
```

## Démarrage rapide

1. Place `generer_calque.py` et le `kwikset.json` de la version française dans le même dossier.
2. Ouvre `kwikset.json` dans un éditeur de texte.
3. Dans `variables_utiles`, modifie `nom_calque` pour choisir le nom du PNG.
4. Renseigne les hauteurs de coupe dans `hauteurs_depuis_dos_pouces`. Chaque étiquette identifie un niveau ; sa valeur est la hauteur mesurée depuis le dos, en pouces.
5. Ajuste au besoin `pixels_par_pouce` et `longueur_lignes_pouces`.
6. Enregistre le JSON et lance :

```bash
python generer_calque.py
```

Le PNG est enregistré dans le même dossier que le JSON. Une fois le nom et les hauteurs renseignés, et l’échelle vérifiée, tout devrait aller comme sur des roulettes !

## Variables utiles

Le groupe `variables_utiles` contient les paramètres principaux :

| Paramètre | Type attendu | Rôle |
| --- | --- | --- |
| `nom_calque` | Texte | Nom du fichier PNG, sans extension. |
| `pixels_par_pouce` | Nombre strictement positif | Échelle du dessin. |
| `longueur_lignes_pouces` | Nombre strictement positif | Longueur commune des lignes horizontales, en pouces. |
| `hauteurs_depuis_dos_pouces` | Objet | Étiquettes et hauteurs numériques positives ou nulles, en pouces. |

Exemple du groupe complet :

```json
"variables_utiles": {
  "nom_calque": "Mon_calque_Kwikset",
  "pixels_par_pouce": 1000,
  "longueur_lignes_pouces": 1.3,
  "hauteurs_depuis_dos_pouces": {
    "1": 0.329,
    "2": 0.306,
    "3": 0.283,
    "4": 0.260,
    "5": 0.237,
    "6": 0.214,
    "7": 0.191
  }
}
```

Ce bloc est un extrait à placer dans l’objet principal du JSON, pas un fichier JSON complet. Il produira un fichier nommé `Mon_calque_Kwikset.png`. Tu peux conserver la section `_aide` du fichier fourni.

Les lignes ne dépendent pas des positions depuis l’épaulement. Il suffit d’ajuster `longueur_lignes_pouces` pour obtenir des lignes assez longues.

## Variables esthétiques

Le groupe `variables_esthetiques` contrôle l’apparence :

- `couleur_rgba` : couleur des lignes et des textes.
- `fond_rgba` : couleur et transparence du fond.
- `epaisseur_px` : épaisseur des lignes, entier d’au moins 1 pixel.
- `marge_gauche_px`, `marge_droite_px`, `marge_haut_px`, `marge_bas_px` : marges en pixels, entiers positifs ou nuls.
- `afficher_dos` : `true` ou `false` pour afficher ou masquer la référence du dos.
- `texte_dos` : texte de cette référence.
- `dos_texte_dx_px`, `dos_texte_dy_px` : décalages du texte du dos, en pixels.
- `afficher_valeurs` : `true` pour utiliser `format_etiquette`, ou `false` pour afficher seulement les noms des niveaux.
- `format_etiquette` : format des étiquettes, par exemple `"{nom}  {hauteur:.3f} in"`.
- `etiquette_dx_px`, `etiquette_dy_px` : décalages des étiquettes, en pixels.
- `police` : objet contenant `fichier` (`null` pour la police intégrée, sinon un chemin de fichier TTF) et `taille_px` (entier d’au moins 1).

Les décalages acceptent des entiers négatifs ou positifs. Les couleurs RGBA sont des listes de quatre entiers entre 0 et 255 : rouge, vert, bleu et opacité. Une opacité de 0 est transparente ; 255 est opaque.

Augmente les marges si les textes sont coupés. Les sections `_aide` expliquent les paramètres et ne sont pas utilisées pour le dessin.

## Points à vérifier

- Utilise un point décimal : `0.329`, pas une virgule décimale.
- Mets les noms et étiquettes entre guillemets doubles, mais pas les valeurs numériques.
- Respecte la syntaxe JSON : pas de commentaires ni de virgules finales.
- Les mots `true`, `false` et `null` font partie de la syntaxe JSON : ne les traduis pas.
- Les hauteurs sont mesurées depuis le dos ; ce ne sont pas des profondeurs mesurées depuis le bord opposé.
- Pour superposer le PNG à une image, fais correspondre leurs échelles. Un redimensionnement modifie l’échelle affichée.
- Ne mélange pas le script français avec le JSON de la version anglaise.

## Autre fichier de configuration

Pour utiliser un autre JSON compatible avec la version française :

```bash
python generer_calque.py ma_configuration.json
```

## Avis d’utilisation

Pour utilisation éducative uniquement.
