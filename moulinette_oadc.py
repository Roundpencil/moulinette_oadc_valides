from os.path import sep

import pandas as pd
from datetime import *

import re
import unicodedata

def respecte_le_format(valeur)->str:
    # 1. Vérifier valeur nulle
    if pd.isna(valeur):
        return ", La ligne est vide"

    # Convertir en string si nécessaire
    valeur = str(valeur)

    if len(valeur) > 11:
        return ", plus de 11 caractères"

    # 2. Interdire espaces ou caractères invisibles en début/fin
    # strip() enlève espaces standards, on compare à l'original
    if valeur != valeur.strip():
        return ", Présence d'espaces au début ou à la fin"

    # 3. Interdire caractères non ASCII (accentués, barrés, etc.)
    try:
        valeur.encode('ascii')
    except UnicodeEncodeError:
        return ", Présence de caractères accentués, invisibles ou barrés"

    # 4. Interdire caractères invisibles internes (catégories Unicode "C")
    for char in valeur:
        if unicodedata.category(char).startswith("C"):
            return ", Présence de caractères invisibles ou peu visibles"

    # 5. Interdire caractères spéciaux consécutifs
    # On considère spécial = non alphanumérique
    if re.search(r'[^a-zA-Z0-9]{2,}', valeur):
        return ", Présence de deux caractères spéciaux consécutifs"

    return ""

# def respecte_le_format(valeur):
#     # Ta fonction existante (exemple simple ici)
#     if pd.isna(valeur):
#         return False
#     return str(valeur).isalnum()


def controler_donnees(chemin_ref, chemin_test, colonne_nom_ref, colonne_nom_test, dossier_sortie=r'.', verbose=True):
    # 1. Chargement des données
    df_ref = pd.read_excel(chemin_ref)
    # if chemin_ref.endswith(".csv"):
    #     df_ref = pd.read_csv(chemin_ref, sep=None, engine='python')
    # elif chemin_ref.endswith(".xlsx") or chemin_ref.endswith(".xls"):
    #     df_ref = pd.read_excel(chemin_ref)
    # else:
    #     return "Format du fichier de référence non reconnu"

    df_test = pd.read_excel(chemin_test)

    # On transforme la colonne de référence en 'set' pour une recherche ultra-rapide
    valeurs_valides_ref = set(df_ref[colonne_nom_ref].astype(str))

    valides = []
    invalides = []

    # 2. Itération et contrôle
    for index, row in df_test.iterrows():
        valeur = str(row[colonne_nom_test])
        raison = ""
        if verbose:
            print(f"Valeur testée : {valeur}")

        # Test 1 : Présence dans le fichier de référence
        if valeur not in valeurs_valides_ref:
            raison += ", Valeur absente du fichier de référence"

        # Test 2 : Respect du format
        raison += respecte_le_format(valeur)
        # elif not respecte_le_format(valeur):
        #     raison += ", Format invalide (critères fonction respecte_le_format)"

        if verbose:
            print(f"\tRaison = {raison}")

        # Dispatching
        raison = raison[2:]
        if raison == "":
            valides.append(row)
        else:
            # On ajoute la raison de l'invalidité
            ligne_err = row.to_dict()
            ligne_err['raison_invalidite'] = raison
            invalides.append(ligne_err)

    fin = datetime.now()
    date_formattee = fin.strftime("sortie_%Y-%m-%d_%H-%M-%S")

    # 3. Export des résultats
    pd.DataFrame(valides).to_excel(f"{dossier_sortie}/lignes_valides_{date_formattee}.xlsx",
                                   index=False)
    pd.DataFrame(invalides).to_excel(f"{dossier_sortie}/lignes_invalides_{date_formattee}.xlsx",
                                     index=False)

    print(f"Traitement terminé. {len(valides)} valides, {len(invalides)} invalides.")
    return ""

# Utilisation
# controler_donnees("reference.xlsx", "a_controler.xlsx", "NomDeLaColonne")