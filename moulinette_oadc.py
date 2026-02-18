import pandas as pd
from datetime import *

def respecte_le_format(valeur):
    # Ta fonction existante (exemple simple ici)
    if pd.isna(valeur):
        return False
    return str(valeur).isalnum()


def controler_donnees(chemin_ref, chemin_test, colonne_nom_ref, colonne_nom_test, dossier_sortie=r'.', verbose=True):
    # 1. Chargement des données
    df_ref = pd.read_excel(chemin_ref)
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
        elif not respecte_le_format(valeur):
            raison += ", Format invalide (critères fonction respecte_le_format)"

        if verbose:
            print(f"\tRaison = {raison}")

        # Dispatching
        if raison == "":
            valides.append(row)
        else:
            # On ajoute la raison de l'invalidité
            ligne_err = row.to_dict()
            ligne_err['raison_invalidite'] = raison[2:]
            invalides.append(ligne_err)

    fin = datetime.now()
    date_formattee = fin.strftime("sortie_%Y-%m-%d_%H-%M-%S")

    # 3. Export des résultats
    pd.DataFrame(valides).to_excel(f"{dossier_sortie}/lignes_valides_{date_formattee}.xlsx",
                                   index=False)
    pd.DataFrame(invalides).to_excel(f"{dossier_sortie}/lignes_invalides_{date_formattee}.xlsx",
                                     index=False)

    print(f"Traitement terminé. {len(valides)} valides, {len(invalides)} invalides.")

# Utilisation
# controler_donnees("reference.xlsx", "a_controler.xlsx", "NomDeLaColonne")