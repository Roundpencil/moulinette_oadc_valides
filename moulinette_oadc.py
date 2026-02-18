import pandas as pd


def respecte_le_format(valeur):
    # Ta fonction existante (exemple simple ici)
    if pd.isna(valeur):
        return False
    return str(valeur).isalnum()


def controler_donnees(chemin_ref, chemin_test, colonne_nom_ref, colonne_nom_test):
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

        # Test 1 : Présence dans le fichier de référence
        if valeur not in valeurs_valides_ref:
            raison = "Valeur absente du fichier de référence"

        # Test 2 : Respect du format
        elif not respecte_le_format(valeur):
            raison = "Format invalide (critères fonction respecte_le_format)"

        # Dispatching
        if raison == "":
            valides.append(row)
        else:
            # On ajoute la raison de l'invalidité
            ligne_err = row.to_dict()
            ligne_err['raison_invalidite'] = raison
            invalides.append(ligne_err)

    # 3. Export des résultats
    pd.DataFrame(valides).to_excel("lignes_valides.xlsx", index=False)
    pd.DataFrame(invalides).to_excel("lignes_invalides.xlsx", index=False)

    print(f"Traitement terminé. {len(valides)} valides, {len(invalides)} invalides.")

# Utilisation
# controler_donnees("reference.xlsx", "a_controler.xlsx", "NomDeLaColonne")