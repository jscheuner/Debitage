import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import os

from debitage import (
    optimize_cutting_ffd,
    optimize_cutting_bfd,
    optimize_cutting_limited_permutations,
    generate_cutting_pdf,
    display_cutting_result_shell,
    group_pieces
)


import tkinter as tk
from tkinter import ttk, messagebox

# Fonction pour extraire les pièces à partir du texte entré
def get_pieces_from_text(text):
    pieces = []
    # Séparer les lignes
    lines = text.strip().split('\n')
    for line in lines:
        # Séparer les colonnes par une tabulation ou un espace
        parts = line.split()
        if len(parts) == 2:
            quantity = int(parts[0])
            length = int(parts[1])
            pieces.append((length, quantity))
    return pieces


def run_optimization(method):
    # Convertir les IntVar en valeurs entières
    bar_length = int(bar_length_var.get())
    blade_width = int(blade_width_var.get())
    clearance = int(clearance_var.get())
    min_waste = int(min_waste_var.get())

    # Récupérer les pièces depuis le champ texte
    pieces = get_pieces_from_text(pieces_text.get("1.0", tk.END).strip())

    if method == '1':  # Simple
        bar_usage = optimize_cutting_ffd(pieces, bar_length, blade_width, clearance, min_waste)
    elif method == '2':  # Optimisé
        bar_usage = optimize_cutting_bfd(pieces, bar_length, blade_width, clearance, min_waste)
    else:  # Optimisé +
        bar_usage, min_waste = optimize_cutting_limited_permutations(pieces, bar_length, blade_width, clearance, min_waste, max_permutations=1000, debug=True)

    # Afficher le résultat dans le champ de texte
    result_display.delete("1.0", tk.END)
    result_display.insert(tk.END, display_cutting_result_shell(bar_usage, bar_length, blade_width, clearance))
    
     # Mettre à jour le label de résultat pour indiquer que l'optimisation a réussi
    result_text.set("L'optimisation a été effectuée avec succès.")


# Fonction pour générer le PDF
def generate_pdf():
    # Récupérer les pièces depuis le champ texte
    pieces = get_pieces_from_text(pieces_text.get("1.0", tk.END).strip())

    # Utiliser les paramètres actuels pour générer le PDF
    bar_length = int(bar_length_var.get())
    blade_width = int(blade_width_var.get())
    clearance = int(clearance_var.get())
    min_waste = int(min_waste_var.get())

    # Appeler la fonction d'optimisation pour calculer l'utilisation des barres
    method = optimization_choice.get().split('.')[0]
    
    if method == '1':  # Simple
        bar_usage = optimize_cutting_ffd(pieces, bar_length, blade_width, clearance, min_waste)
    elif method == '2':  # Optimisé
        bar_usage = optimize_cutting_bfd(pieces, bar_length, blade_width, clearance, min_waste)
    else:  # Optimisé +
        bar_usage, min_waste = optimize_cutting_limited_permutations(pieces, bar_length, blade_width, clearance, min_waste, max_permutations=1000, debug=True)

    # Nom du fichier PDF à générer
    pdf_filename = "debitage_resultat.pdf"
    
    # Générer le PDF avec les résultats calculés
    generate_cutting_pdf(bar_usage=bar_usage, bar_length=bar_length, blade_width=blade_width, clearance=clearance, pieces=pieces, filename=pdf_filename)
    

    # Afficher un message de succès dans le label de résultat
    result_text.set("Le PDF a été généré avec succès.")
    
    # Ouvrir automatiquement le fichier PDF
    try:
        os.startfile(pdf_filename)  # Ouvrir le fichier PDF avec l'application par défaut (Windows)
    except Exception as e:
        result_display.insert(tk.END, f"\nErreur lors de l'ouverture du PDF: {e}")




# Fonction pour ajouter un texte d'invite (placeholder) au champ de texte
def add_placeholder(pieces_text, placeholder):
    pieces_text.insert(tk.END, placeholder)
    pieces_text.config(fg='grey')

    def remove_placeholder(event):
        if pieces_text.get("1.0", tk.END).strip() == placeholder:
            pieces_text.delete("1.0", tk.END)
            pieces_text.config(fg='black')

    def add_placeholder_back(event):
        if pieces_text.get("1.0", tk.END).strip() == "":
            pieces_text.insert(tk.END, placeholder)
            pieces_text.config(fg='grey')

    pieces_text.bind("<FocusIn>", remove_placeholder)
    pieces_text.bind("<FocusOut>", add_placeholder_back)

# Fonction pour centrer la fenêtre et ajuster sa hauteur visible
def center_window(root):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 800
    window_height = int(screen_height * 0.9)

    position_x = int((screen_width - window_width) / 2)
    position_y = 0

    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Fonction pour l'optimisation
def run_optimization(method):
    # Convertir les IntVar en valeurs entières
    bar_length = int(bar_length_var.get())
    blade_width = int(blade_width_var.get())
    clearance = int(clearance_var.get())
    min_waste = int(min_waste_var.get())

    pieces = get_pieces_from_text(pieces_text.get("1.0", tk.END).strip())  # Récupérer les pièces

    if method == '1':  # Simple
        bar_usage = optimize_cutting_ffd(pieces, bar_length, blade_width, clearance, min_waste)
    elif method == '2':  # Optimisé
        bar_usage = optimize_cutting_bfd(pieces, bar_length, blade_width, clearance, min_waste)
    else:  # Optimisé +
        bar_usage, min_waste = optimize_cutting_limited_permutations(pieces, bar_length, blade_width, clearance, min_waste, max_permutations=1000, debug=True)

    # Afficher le résultat dans le champ de texte
    result_display.delete("1.0", tk.END)  # Effacer le texte précédent
    result_display.insert(tk.END, display_cutting_result_shell(bar_usage, bar_length, blade_width, clearance))  # Afficher le résultat

    # Mettre à jour le label de résultat pour indiquer que l'optimisation a réussi
    result_text.set("L'optimisation a été effectuée avec succès.")
    
# Initialiser la fenêtre principale
root = tk.Tk()
root.title("Optimisation du Débitage")

# Centrer la fenêtre et ajuster la hauteur
center_window(root)

# Variables globales
bar_length_var = tk.IntVar(value=6000)  # Longueur des barres
blade_width_var = tk.IntVar(value=5)    # Largeur de la lame
clearance_var = tk.IntVar(value=30)     # Affranchissement
min_waste_var = tk.IntVar(value=20)     # Chute minimale

result_text = tk.StringVar()

# Créer un label pour l'affichage du choix
label = tk.Label(root, text="Choisissez une méthode d'optimisation :")
label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Créer les options de sélection
optimization_choice = ttk.Combobox(root, values=["1. Simple (FFD)", "2. Optimisé (BFD)", "3. Optimisé + (Permutations)"])
optimization_choice.grid(row=0, column=1, padx=10, pady=10, sticky='w')
optimization_choice.set("2. Optimisé (BFD)")

# Paramètres d'optimisation
tk.Label(root, text="Longueur de la barre :").grid(row=1, column=0, sticky='w', padx=10, pady=5)
bar_length_entry = tk.Entry(root, textvariable=bar_length_var)
bar_length_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Épaisseur de la lame :").grid(row=2, column=0, sticky='w', padx=10, pady=5)
blade_width_entry = tk.Entry(root, textvariable=blade_width_var)
blade_width_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Affranchissement :").grid(row=3, column=0, sticky='w', padx=10, pady=5)
clearance_entry = tk.Entry(root, textvariable=clearance_var)
clearance_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Chute minimale :").grid(row=4, column=0, sticky='w', padx=10, pady=5)
min_waste_entry = tk.Entry(root, textvariable=min_waste_var)
min_waste_entry.grid(row=4, column=1, padx=10, pady=5)

# Créer un champ texte pour la saisie des pièces avec un scroll
pieces_text = tk.Text(root, height=10, undo=True)
pieces_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Ajouter un placeholder
add_placeholder(pieces_text, "Entrez le nombre de pièces et la longueur (ex : 2\t5625)")

# Zone de texte pour afficher le résultat de l'optimisation avec un scroll
result_display = tk.Text(root, height=10)
result_display.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Ajouter le label pour afficher les messages de résultat
result_label = tk.Label(root, textvariable=result_text, fg="green", anchor="w")
result_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='w')

# Boutons pour lancer l'optimisation et générer le PDF
run_button = tk.Button(root, text="Lancer l'optimisation", command=lambda: run_optimization(optimization_choice.get().split('.')[0]))
run_button.grid(row=7, column=0, padx=10, pady=10, sticky='w')

pdf_button = tk.Button(root, text="Générer PDF", command=generate_pdf)
pdf_button.grid(row=7, column=1, padx=10, pady=10, sticky='w')

# Ajuster les proportions des colonnes et des lignes pour que les éléments s'étendent
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
# root.grid_rowconfigure(7, weight=1)  # Pour le label de résultat

# Lancer la fenêtre
root.mainloop()
