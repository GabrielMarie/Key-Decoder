import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def nombre(valeur, nom, minimum=0, entier=False):
    if isinstance(valeur, bool) or not isinstance(valeur, (int, float)):
        raise ValueError(f"{nom} doit etre un nombre.")
    if not math.isfinite(valeur) or valeur < minimum:
        raise ValueError(f"{nom} doit etre fini et >= {minimum}.")
    if entier and not isinstance(valeur, int):
        raise ValueError(f"{nom} doit etre un entier.")
    return valeur


def creer_calque(cfg, dossier):
    s = nombre(cfg["pixels_par_pouce"], "pixels_par_pouce")
    if s == 0:
        raise ValueError("pixels_par_pouce doit etre > 0.")
    m = nombre(cfg["marge_px"], "marge_px", entier=True)
    e = nombre(cfg["epaisseur_px"], "epaisseur_px", minimum=1, entier=True)
    stations = cfg["positions_depuis_epaulement"]
    niveaux = cfg["hauteurs_depuis_dos"]
    if not isinstance(stations, list) or not stations:
        raise ValueError("positions_depuis_epaulement doit etre une liste non vide.")
    if not isinstance(niveaux, dict) or not niveaux:
        raise ValueError("hauteurs_depuis_dos doit etre un objet non vide.")
    for x in stations:
        nombre(x, "position")
    for h in niveaux.values():
        nombre(h, "hauteur")
    longueur = max(nombre(cfg["longueur_reference"], "longueur_reference"), max(stations))
    hauteur = max(niveaux.values())
    p = cfg["mise_en_page"]
    for nom, valeur in p.items():
        nombre(valeur, nom, minimum=0 if nom.startswith("supplement_") else -math.inf, entier=True)
    couleurs = []
    for nom in ("couleur", "fond_rgba"):
        rgba = cfg[nom]
        if not isinstance(rgba, list) or len(rgba) != 4:
            raise ValueError(f"{nom} doit contenir 4 entiers RGBA.")
        for composante in rgba:
            nombre(composante, nom, entier=True)
            if composante > 255:
                raise ValueError(f"{nom} : chaque composante doit etre <= 255.")
        couleurs.append(tuple(rgba))
    c, fond = couleurs
    taille = nombre(cfg["police"]["taille_px"], "police.taille_px", minimum=1, entier=True)
    fichier_police = cfg["police"]["fichier"]
    if fichier_police is None:
        police = ImageFont.load_default(size=taille)
    else:
        police = ImageFont.truetype(str(dossier / fichier_police), taille)
    textes = cfg["textes"]
    for nom in ("dos", "epaulement", "format_station"):
        if not isinstance(textes[nom], str):
            raise ValueError(f"textes.{nom} doit etre du texte.")
    largeur_px = round(longueur * s) + 2 * m + p["supplement_largeur_px"]
    hauteur_px = round(hauteur * s) + 2 * m + p["supplement_hauteur_px"]
    if largeur_px < 1 or hauteur_px < 1:
        raise ValueError("Les dimensions calculees doivent etre >= 1 pixel.")
    im = Image.new("RGBA", (largeur_px, hauteur_px), fond)
    d = ImageDraw.Draw(im)
    x0, ydos = m, m + round(hauteur * s)
    xfin = m + round(longueur * s)
    d.line((x0, ydos, xfin, ydos), fill=c, width=e)
    d.text((x0 + p["dos_texte_dx_px"], ydos + p["dos_texte_dy_px"]), textes["dos"], fill=c, font=police)
    d.line((x0, m + p["epaulement_haut_dy_px"], x0, ydos + p["epaulement_bas_dy_px"]), fill=c, width=e)
    d.text((x0 + p["epaulement_texte_dx_px"], m + p["epaulement_texte_dy_px"]), textes["epaulement"], fill=c, font=police)
    for i, x in enumerate(stations, 1):
        xp = m + round(x * s)
        d.line((xp, m + p["station_haut_dy_px"], xp, ydos + p["station_bas_dy_px"]), fill=c, width=e)
        d.text((xp + p["station_texte_dx_px"], ydos + p["station_texte_dy_px"]), textes["format_station"].format(numero=i), fill=c, font=police)
    for nom, h in niveaux.items():
        y = ydos - round(h * s)
        d.line((x0, y, xfin, y), fill=c, width=e)
        d.text((xfin + p["niveau_texte_dx_px"], y + p["niveau_texte_dy_px"]), nom, fill=c, font=police)
    destination = dossier / cfg["destination"]
    im.save(destination, format="PNG")
    return destination, im.size


def main():
    parser = argparse.ArgumentParser(description="Genere un calque avec les options du JSON.")
    parser.add_argument("configuration", nargs="?", type=Path,
                        default=Path(__file__).resolve().with_name("corbin_z.json"))
    args = parser.parse_args()
    try:
        chemin = args.configuration.resolve()
        with chemin.open(encoding="utf-8") as f:
            cfg = json.load(f)
        destination, dimensions = creer_calque(cfg, chemin.parent)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        parser.exit(1, f"Erreur de configuration ou de generation : {exc}\n")
    print(f"Calque cree : {destination} ({dimensions[0]} x {dimensions[1]} px)")


if __name__ == "__main__":
    main()
