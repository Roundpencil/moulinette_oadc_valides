import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

import moulinette_oadc


def selectionner_entree():
    # Définition des extensions autorisées
    types_fichiers = [
        ("Fichiers de données", "*.csv *.xlsx"),
        ("Fichiers CSV", "*.csv"),
        ("Fichiers Excel", "*.xlsx")
    ]

    path = filedialog.askopenfilename(
        title="Sélectionnez un fichier d'entrée",
        filetypes=types_fichiers)

    entry_input.delete(0, tk.END)
    entry_input.insert(0, path)


def selectionner_reference():
    types_fichiers = [
        ("Fichiers de données", "*.csv *.xlsx"),
        ("Fichiers CSV", "*.csv"),
        ("Fichiers Excel", "*.xlsx")
    ]

    path = filedialog.askopenfilename(title="Sélectionner le fichier de référence",
                                      filetypes=types_fichiers)

    entry_ref.delete(0, tk.END)
    entry_ref.insert(0, path)


def selectionner_sortie():
    path = filedialog.askdirectory(title="Dossier de sortie")
    entry_output.delete(0, tk.END)
    entry_output.insert(0, path)


def valider():
    # Ici, vous pouvez ajouter votre logique de traitement
    f_in = entry_input.get()
    f_ref = entry_ref.get()
    f_out = entry_output.get()
    nom_colonne_ref = "OADC"
    nom_colonne_test = "OADC"

    print(f"dossier de sortie : {f_out}")

    if f_in and f_ref and f_out:
        messagebox.showinfo("Succès", f"Traitement lancé !\nSortie : {f_out}")
    else:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")

    config = {
        "chemin_fichier_de_reference": f_ref,
        "chemin_de_sortie": f_out,
        "nom_de_la_colonne_entree": nom_colonne_ref,
        "nom_de_la_colonne_de_reference": nom_colonne_ref,
    }

    # Écriture dans un fichier JSON
    with open("config.json", "w", encoding="utf-8") as fichier_json:
        json.dump(config, fichier_json, indent=4, ensure_ascii=False)

    moulinette_oadc.controler_donnees(chemin_ref=f_ref,
                                      chemin_test=f_in,
                                      colonne_nom_ref=nom_colonne_ref,
                                      colonne_nom_test=nom_colonne_test,
                                      dossier_sortie=f_out)


    messagebox.showinfo("Succès", f"Fin du traitement !\nSortie : {f_out}")

def charger_config(chemin="config.json"):
    if os.path.exists(chemin):
        with open(chemin, "r", encoding="utf-8") as fichier_json:
            config = json.load(fichier_json)
        return config
    else:
        print("Le fichier config.json n'existe pas.")
        return dict()

# Configuration de la fenêtre principale
root = tk.Tk()
root.title("Moulinette af2m OADC")
root.geometry("500x250")

config = charger_config()
print(f"Config = {config}")

# Fichier d'entrée
tk.Label(root, text="Fichier d'entrée :").pack(pady=(10, 0))
entry_input = tk.Entry(root, width=50)
entry_input.insert(0, config.get("chemin_fichier_de_reference", ""))
entry_input.pack()
tk.Button(root, text="Parcourir...", command=selectionner_entree).pack()

# Fichier de référence
tk.Label(root, text="Fichier de référence :").pack(pady=(10, 0))
entry_ref = tk.Entry(root, width=50)
entry_ref.pack()
tk.Button(root, text="Parcourir...", command=selectionner_reference).pack()

# Dossier de sortie
tk.Label(root, text="Dossier de sortie :").pack(pady=(10, 0))
entry_output = tk.Entry(root, width=50)
entry_output.insert(0, config.get("chemin_de_sortie", ""))
entry_output.pack()
tk.Button(root, text="Parcourir...", command=selectionner_sortie).pack()

# Bouton de validation
tk.Button(root, text="Lancer", bg="green", fg="white", command=valider).pack(pady=20)

root.mainloop()

# # Test de la fonction
# fichier = selectionner_fichier()
# print(f"Fichier sélectionné : {fichier}")