import matplotlib.pyplot as plt
import itertools
import random
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle

# # Longueur de la barre
# bar_length = 6000
# # Épaisseur de la lame
# blade_width = 5
# # Affranchissement (espace à laisser en début et en fin de barre)
# clearance = 30
# # Chute minimale
# min_waste = 20

# Liste des pièces à découper (longueur de chaque pièce et quantité)
# pieces = [
#     (1550, 2),
#     (1000, 3),
#     (150, 5),
#     (758, 18),
#     (1256, 4),
#     (3600, 5),
#     (4260, 1),
#     (1760, 4),
#     (1050, 6),
#     (20, 100),
    
# ]

# Fonction pour calculer le débitage ffd
def optimize_cutting_ffd(pieces, bar_length, blade_width, clearance, min_waste):
    # Créer une liste de toutes les pièces à découper (chaque pièce représentée individuellement)
    all_pieces = []
    for length, quantity in pieces:
        all_pieces.extend([length] * quantity)
    
    # Trier les pièces par ordre décroissant pour appliquer la stratégie FFD
    all_pieces.sort(reverse=True)
    
    bar_usage = []
    
    while all_pieces:
        current_bar = []
        remaining_length = bar_length - clearance * 2
        i = 0
        while i < len(all_pieces):
            piece = all_pieces[i]
            
            # Vérifier s'il reste assez de place pour la pièce ET pour la chute minimale
            if remaining_length >= piece + blade_width + min_waste:
                current_bar.append(piece)
                remaining_length -= piece + blade_width
                all_pieces.pop(i)  # Enlever la pièce placée
            else:
                i += 1  # Passer à la pièce suivante si elle ne rentre pas
        
        # Ajouter la barre pleine
        bar_usage.append(current_bar)
    
    return bar_usage


def optimize_cutting_bfd(pieces, bar_length, blade_width, clearance, min_waste):
    # Créer une liste de toutes les pièces à découper (chaque pièce représentée individuellement)
    all_pieces = []
    for length, quantity in pieces:
        all_pieces.extend([length] * quantity)
    
    # Trier les pièces par ordre décroissant (Best Fit Decreasing)
    all_pieces.sort(reverse=True)
    
    # Liste des barres utilisées
    bar_usage = []
    
    for piece in all_pieces:
        best_bar = None
        best_fit_waste = float('inf')
        
        # Chercher la meilleure barre où la pièce peut rentrer
        for bar in bar_usage:
            remaining_length = bar_length - clearance * 2 - sum(bar) - (len(bar) * blade_width)
            
            # Vérifier s'il reste suffisamment de place pour la pièce ET pour respecter la chute minimale
            if remaining_length >= piece + min_waste and remaining_length - piece < best_fit_waste:
                best_bar = bar
                best_fit_waste = remaining_length - piece
        
        # Si aucune barre existante ne peut contenir la pièce, on commence une nouvelle barre
        if best_bar is None:
            bar_usage.append([piece])
        else:
            best_bar.append(piece)
    
    return bar_usage



def optimize_cutting_limited_permutations(pieces, bar_length, blade_width, clearance, min_waste, max_permutations=100, debug=False):
    max_permutations=10000
    debug=False
    print(max_permutations)
    # Créer une liste de toutes les pièces à découper (chaque pièce représentée individuellement)
    all_pieces = []
    for length, quantity in pieces:
        all_pieces.extend([length] * quantity)
    
    # Meilleure solution
    best_solution = None
    min_total_waste = float('inf')
    
    # Générer un nombre limité de permutations aléatoires
    tested_permutations = set()
    iteration = 0
    while len(tested_permutations) < max_permutations:
        iteration += 1
        perm = tuple(random.sample(all_pieces, len(all_pieces)))
        if perm in tested_permutations:
            continue
        tested_permutations.add(perm)
        
        if debug:
            print(f"Test permutation {iteration}/{max_permutations}: {perm}")
        
        bar_usage = []
        current_bar = []
        remaining_length = bar_length - clearance * 2
        
        for piece in perm:
            if remaining_length >= piece + blade_width:
                current_bar.append(piece)
                remaining_length -= piece + blade_width
            else:
                # Ajouter la barre pleine et commencer une nouvelle
                bar_usage.append(current_bar)
                current_bar = [piece]
                remaining_length = bar_length - clearance * 2 - piece - blade_width
        
        # Ajouter la dernière barre utilisée
        if current_bar:
            bar_usage.append(current_bar)
        
        # Calculer la chute totale pour cette solution
        total_waste = 0
        for bar in bar_usage:
            total_piece_length = sum(bar) + (len(bar) - 1) * blade_width
            remaining_length = bar_length - clearance * 2 - total_piece_length
            total_waste += remaining_length
        
        if debug:
            print(f"  Chute totale pour cette permutation: {total_waste:.2f}mm")
        
        # Si cette solution est meilleure, la conserver
        if total_waste < min_total_waste:
            min_total_waste = total_waste
            best_solution = bar_usage
            
            if debug:
                print(f"  Nouvelle solution optimale trouvée avec {len(best_solution)} barres et {min_total_waste:.2f}mm de chute.")
    
    return best_solution, min_total_waste



# def draw_bars(bar_usage, bar_length, clearance, blade_width, min_waste):
#     fig, ax = plt.subplots(figsize=(10, len(bar_usage)))
    
#     for i, bar in enumerate(bar_usage):
#         start = clearance
#         y_pos = len(bar_usage) - i - 1
#         for piece in bar:
#             ax.broken_barh([(start, piece)], (y_pos - 0.4, 0.8), facecolors='tab:blue')
#             start += piece + blade_width
        
#         # Ajouter la chute à la fin de la barre
#         waste_length = bar_length - start - clearance
#         if waste_length >= min_waste:
#             ax.broken_barh([(start, waste_length)], (y_pos - 0.4, 0.8), facecolors='tab:red')
    
#     ax.set_xlim(0, bar_length)
#     ax.set_ylim(-1, len(bar_usage))
#     ax.set_xlabel('Longueur (mm)')
#     ax.set_yticks([i for i in range(len(bar_usage))])
#     ax.set_yticklabels([f"Barre {i+1}" for i in range(len(bar_usage))])
#     ax.grid(True)
    
#     plt.show()

def group_pieces(pieces):
    """Fonction pour regrouper les pièces identiques consécutives."""
    grouped_pieces = []
    current_piece = pieces[0]
    count = 1
    
    for piece in pieces[1:]:
        if piece == current_piece:
            count += 1
        else:
            if count > 1:
                grouped_pieces.append(f"{count} pièces de {current_piece}mm")
            else:
                grouped_pieces.append(f"{current_piece}mm")
            current_piece = piece
            count = 1
    
    # Ajouter la dernière série de pièces
    if count > 1:
        grouped_pieces.append(f"{count} pièces de {current_piece}mm")
    else:
        grouped_pieces.append(f"{current_piece}mm")
    
    return ", ".join(grouped_pieces)


# def display_cutting_result_shell(bar_usage, bar_length, blade_width, clearance):
#     # Calculer la largeur maximale des pièces (colonne centrale) après regroupement
#     max_pieces_len = max([len(group_pieces(bar)) for bar in bar_usage])
#     pieces_col_width = max(max_pieces_len, 45)  # Largeur minimale de 45 si toutes les barres sont petites
#     bar_col_width = 10
#     chute_col_width = 15  # Augmenter un peu pour permettre l'affichage des chutes
    
#     # Calcul de la chute totale
#     total_waste = 0
#     total_bars_used = len(bar_usage)

#     # Fonction pour construire une ligne avec des bordures et du texte centré
#     def print_line(char='-', length=bar_col_width + pieces_col_width + chute_col_width + 4):  # Ajustement de la longueur de ligne
#         print(char * length)
    
#     def print_row(bar, pieces, chute):
#         bar_str = f"{bar}".center(bar_col_width)
#         pieces_str = f"{pieces}".ljust(pieces_col_width)
#         chute_str = f"{chute}".center(chute_col_width)
#         print(f"|{bar_str}|{pieces_str}|{chute_str}|")

#     # En-tête du tableau
#     print_line()
#     print_row("Barre", "Pièces (Longueurs)", "Chute")
#     print_line()
    
#     # Construire les lignes de résultats
#     for i, bar in enumerate(bar_usage):
#         total_piece_length = sum(bar) + (len(bar) - 1) * blade_width
#         remaining_length = bar_length - clearance * 2 - total_piece_length
        
#         # Accumuler la chute totale
#         total_waste += remaining_length
        
#         # Grouper les pièces similaires avant de les afficher
#         grouped_pieces = group_pieces(bar)
        
#         # Afficher chaque barre avec ses pièces regroupées et la chute
#         print_row(f"Barre {i + 1}", grouped_pieces, f"{remaining_length}mm")
    
#     # Ligne de fin de tableau
#     print_line()
    
#     # Calcul du pourcentage de chute totale
#     total_material = total_bars_used * bar_length
#     waste_percentage = (total_waste / total_material) * 100
    
#     # Afficher le nombre de barres utilisées, la chute totale et le pourcentage
#     print(f"\n{total_bars_used} barres --> Chute totale : {total_waste:.2f}mm sur {total_material}mm ({waste_percentage:.2f}%)")

def display_cutting_result_shell(bar_usage, bar_length, blade_width, clearance):
    """Retourne le résultat sous forme de texte au lieu de l'imprimer dans le terminal."""
    result = []
    
    # Calculer la largeur maximale des pièces (colonne centrale) après regroupement
    max_pieces_len = max([len(group_pieces(bar)) for bar in bar_usage])
    pieces_col_width = max(max_pieces_len, 45)  # Largeur minimale de 45 si toutes les barres sont petites
    bar_col_width = 10
    chute_col_width = 15  # Augmenter un peu pour permettre l'affichage des chutes
    
    # Calcul de la chute totale
    total_waste = 0
    total_bars_used = len(bar_usage)

    # Fonction pour construire une ligne avec des bordures
    def print_line(char='-', length=bar_col_width + pieces_col_width + chute_col_width + 4):
        result.append(char * length)
    
    def print_row(bar, pieces, chute):
        bar_str = f"{bar}".center(bar_col_width)
        pieces_str = f"{pieces}".ljust(pieces_col_width)
        chute_str = f"{chute}".center(chute_col_width)
        result.append(f"|{bar_str}|{pieces_str}|{chute_str}|")

    # En-tête du tableau
    print_line()
    print_row("Barre", "Pièces (Longueurs)", "Chute")
    print_line()
    
    # Construire les lignes de résultats
    for i, bar in enumerate(bar_usage):
        total_piece_length = sum(bar) + (len(bar) - 1) * blade_width
        remaining_length = bar_length - clearance * 2 - total_piece_length
        
        # Accumuler la chute totale
        total_waste += remaining_length
        
        # Grouper les pièces similaires avant de les afficher
        grouped_pieces = group_pieces(bar)
        
        # Ajouter chaque barre avec ses pièces regroupées et la chute au résultat
        print_row(f"Barre {i + 1}", grouped_pieces, f"{remaining_length}mm")
    
    # Ligne de fin de tableau
    print_line()
    
    # Calcul du pourcentage de chute totale
    total_material = total_bars_used * bar_length
    waste_percentage = (total_waste / total_material) * 100
    
    result.append(f"\n{total_bars_used} barres --> Chute totale : {total_waste:.2f}mm sur {total_material}mm ({waste_percentage:.2f}%)")

    return "\n".join(result)


from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def generate_cutting_pdf(bar_usage, bar_length, blade_width, clearance, pieces, filename="debitage_large.pdf"):
    """Génère un PDF avec la liste des pièces et les résultats d'optimisation."""
    # Utiliser un format paysage
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    margin = 20 * mm  # Marge standard

    # Largeur totale disponible pour le tableau (sans marges)
    total_table_width = width - 2 * margin  # On enlève la marge des deux côtés
    
    # Répartition des colonnes (on veut que la colonne "Pièces" prenne plus d'espace)
    bar_col_width = total_table_width * 0.15  # 15% pour "Barre"
    chute_col_width = total_table_width * 0.15  # 15% pour "Chute"
    pieces_col_width = total_table_width * 0.70  # 70% pour "Pièces (Longueurs)"

    # Hauteur disponible pour le contenu après le titre
    y_position = height - 25 * mm  # Espace pour le titre
    line_height = 7 * mm  # Hauteur de chaque ligne

    # Ajouter la liste de débitage avant le tableau des résultats d'optimisation
    c.setFont("Helvetica", 12)
    c.drawString(margin, y_position, "Liste de débitage :")
    y_position -= 10 * mm  # Laisser de l'espace après le titre

    # Afficher la liste des pièces dans le PDF
    for length, quantity in pieces:
        c.drawString(margin, y_position, f"{quantity} pièces de {length}mm")
        y_position -= line_height

        # Si la hauteur restante ne suffit plus, on passe à une nouvelle page
        if y_position < margin:
            c.showPage()  # Ajouter une nouvelle page
            y_position = height - margin  # Réinitialiser y_position après le saut de page

    # Ajouter de l'espace après la liste de débitage
    y_position -= 15 * mm

    # Ajouter le titre du tableau des résultats d'optimisation
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y_position, "Tableau des résultats d'optimisation :")
    y_position -= 10 * mm  # Laisser de l'espace après le titre

    # Construire les données du tableau
    data = [["Barre", "Pièces (Longueurs)", "Chute"]]
    
    # Ajouter les barres et leurs pièces
    for i, bar in enumerate(bar_usage):
        total_piece_length = sum(bar) + (len(bar) - 1) * blade_width
        remaining_length = bar_length - clearance * 2 - total_piece_length

        # Grouper les pièces similaires
        grouped_pieces = group_pieces(bar)

        # Ajouter les informations à la table
        data.append([f"Barre {i + 1}", grouped_pieces, f"{remaining_length}mm"])

    # Style de la table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ])

    
    # Diviser les lignes du tableau et les ajouter progressivement avec vérification de la hauteur disponible
    for row in data:
        table = Table([row], colWidths=[bar_col_width, pieces_col_width, chute_col_width])
        table.setStyle(table_style)

        # Appeler wrapOn pour calculer l'espace pris par le tableau
        table_width, table_height = table.wrapOn(c, width, height)

        # Si pas assez de place pour la ligne sur la page actuelle, ajouter une nouvelle page
        if y_position - table_height < margin:
            c.showPage()
            y_position = height - margin  # Réinitialiser pour la nouvelle page

        # Dessiner le tableau
        table.drawOn(c, margin, y_position - table_height)
        y_position -= table_height  # Mettre à jour y_position après avoir dessiné le tableau

    # Enregistrer le fichier PDF
    c.save()


def main():
    print("Choisissez une méthode d'optimisation :")
    print("1. Simple (First Fit Decreasing)")
    print("2. Optimisé (Best Fit Decreasing)")
    print("3. Optimisé + (Permutations aléatoires)")
    
    choice = input("Entrez le numéro de l'optimisation souhaitée (1/2/3) : ")

    if choice == '1':
        print("Vous avez choisi l'optimisation Simple (FFD).")
        bar_usage = optimize_cutting_ffd(pieces, bar_length, blade_width, clearance, min_waste)
    elif choice == '2':
        print("Vous avez choisi l'optimisation Optimisé (BFD).")
        bar_usage = optimize_cutting_bfd(pieces, bar_length, blade_width, clearance, min_waste)
    elif choice == '3':
        print("Vous avez choisi l'optimisation Optimisé + (Permutations aléatoires).")
        bar_usage, min_waste_found = optimize_cutting_limited_permutations(pieces, bar_length, blade_width, clearance, min_waste, max_permutations=1000, debug=True)
    else:
        print("Choix invalide. Utilisation de l'optimisation par défaut (FFD).")
        bar_usage = optimize_cutting_ffd(pieces, bar_length, blade_width, clearance, min_waste)
    
    # Afficher les résultats dans le shell
    display_cutting_result_shell(bar_usage, bar_length, blade_width, clearance)

    # Générer le PDF
    generate_cutting_pdf(bar_usage, bar_length, blade_width, clearance)

if __name__ == "__main__":
    main()

