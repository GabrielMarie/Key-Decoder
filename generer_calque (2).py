import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def nombre(v, nom, minimum=0, entier=False, strict=False):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(f"{nom} : nombre fini attendu.")
    if v < minimum or (strict and v == minimum):
        raise ValueError(f"{nom} : valeur {'>' if strict else '>='} {minimum} attendue.")
    if entier and not isinstance(v, int):
        raise ValueError(f"{nom} : entier attendu.")
    return v


def booleen(v, nom):
    if not isinstance(v, bool):
        raise ValueError(f"{nom} : true ou false attendu.")
    return v


def couleur(v, nom):
    if not isinstance(v, list) or len(v) != 4:
        raise ValueError(f"{nom} : liste de 4 entiers RGBA attendue.")
    for composante in v:
        nombre(composante, nom, entier=True)
        if composante > 255:
            raise ValueError(f"{nom} : composantes entre 0 et 255.")
    return tuple(v)


def creer_calque(cfg, dossier):
    u = cfg["variables_utiles"]
    a = cfg["variables_esthetiques"]
    nom = u["nom_calque"]
    if not isinstance(nom, str) or not nom.strip() or nom in (".", "..") or any(c in nom for c in '<>:"/\\|?*'):
        raise ValueError("nom_calque : nom de fichier simple non vide, sans caracteres reserves.")
    s = nombre(u["pixels_par_pouce"], "pixels_par_pouce", strict=True)
    longueur = nombre(u["longueur_lignes_pouces"], "longueur_lignes_pouces", strict=True)
    niveaux = u["hauteurs_depuis_dos_pouces"]
    if not isinstance(niveaux, dict) or not niveaux:
        raise ValueError("hauteurs_depuis_dos_pouces : objet non vide attendu.")
    for h in niveaux.values():
        nombre(h, "hauteur")
    for cle in ("marge_gauche_px", "marge_droite_px", "marge_haut_px", "marge_bas_px"):
        nombre(a[cle], cle, entier=True)
    for cle in ("dos_texte_dx_px", "dos_texte_dy_px", "etiquette_dx_px", "etiquette_dy_px"):
        nombre(a[cle], cle, minimum=-math.inf, entier=True)
    epaisseur = nombre(a["epaisseur_px"], "epaisseur_px", minimum=1, entier=True)
    afficher_dos = booleen(a["afficher_dos"], "afficher_dos")
    afficher_valeurs = booleen(a["afficher_valeurs"], "afficher_valeurs")
    for cle in ("texte_dos", "format_etiquette"):
        if not isinstance(a[cle], str):
            raise ValueError(f"{cle} : texte attendu.")
    c = couleur(a["couleur_rgba"], "couleur_rgba")
    fond = couleur(a["fond_rgba"], "fond_rgba")
    taille = nombre(a["police"]["taille_px"], "police.taille_px", minimum=1, entier=True)
    fichier = a["police"]["fichier"]
    police = ImageFont.load_default(size=taille) if fichier is None else ImageFont.truetype(str(dossier / fichier), taille)
    x0 = a["marge_gauche_px"]
    xfin = x0 + round(longueur * s)
    ydos = a["marge_haut_px"] + round(max(niveaux.values()) * s)
    largeur = xfin + a["marge_droite_px"] + 1
    hauteur = ydos + a["marge_bas_px"] + 1
    im = Image.new("RGBA", (largeur, hauteur), fond)
    d = ImageDraw.Draw(im)
    if afficher_dos:
        d.line((x0, ydos, xfin, ydos), fill=c, width=epaisseur)
        d.text((x0 + a["dos_texte_dx_px"], ydos + a["dos_texte_dy_px"]), a["texte_dos"], fill=c, font=police)
    for etiquette, h in niveaux.items():
        y = ydos - round(h * s)
        d.line((x0, y, xfin, y), fill=c, width=epaisseur)
        texte = a["format_etiquette"].format(nom=etiquette, hauteur=h) if afficher_valeurs else etiquette
        d.text((xfin + a["etiquette_dx_px"], y + a["etiquette_dy_px"]), texte, fill=c, font=police)
    destination = dossier / (nom if nom.lower().endswith(".png") else nom + ".png")
    im.save(destination, format="PNG")
    return destination, im.size


def main():
    parser = argparse.ArgumentParser(description="Calque de niveaux horizontaux configure dans un JSON.")
    parser.add_argument("configuration", nargs="?", type=Path, default=Path(__file__).resolve().with_name("kwikset.json"))
    args = parser.parse_args()
    try:
        chemin = args.configuration.resolve()
        with chemin.open(encoding="utf-8") as f:
            cfg = json.load(f)
        destination, taille = creer_calque(cfg, chemin.parent)
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError) as exc:
        parser.exit(1, f"Erreur : {exc}\n")
    print(f"Calque cree : {destination} ({taille[0]} x {taille[1]} px)")


if __name__ == "__main__":
    main()
