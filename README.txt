Optimisation du Débitage de Barres

Ce projet est une application Python utilisant Tkinter pour créer une interface graphique permettant d'optimiser le débitage de barres métalliques en minimisant les chutes. L'application génère également un fichier PDF avec les résultats de l'optimisation.

Fonctionnalités

- Saisie des paramètres : Longueur de la barre, épaisseur de la lame, affranchissement, et chute minimale.
- Optimisation des découpes : Utilisation de différentes méthodes pour optimiser le placement des pièces afin de minimiser les chutes.
- Affichage des résultats : Les résultats de l'optimisation sont affichés directement dans l'interface.
- Génération de PDF : Un fichier PDF est généré avec la liste des pièces, les résultats d'optimisation, et les numéros de page.
- Trois méthodes d'optimisation :
  1. Simple (FFD) : First Fit Decreasing.
  2. Optimisé (BFD) : Best Fit Decreasing.
  3. Optimisé + (Permutations) : Recherche avec permutations pour améliorer le résultat PAS ENCORE AU POINT.

Prérequis

- Python 3.x
- Bibliothèques Python : ReportLab, Tkinter, PyInstaller (facultatif pour créer un exécutable)

Installation

1. Clonez le projet depuis GitHub :

   git clone https://github.com/jscheunerr/Debitage.git
   cd nom-du-repo

2. Installez les dépendances :

   pip install -r requirements.txt

Utilisation

1. Exécutez l'application Tkinter :

   python debitage_gui.py

2. Dans l'interface graphique :
   - Entrez les pièces à découper dans le champ de texte au format : quantité <tab> longueur. Exemple :
     2    5625
     10   1500

   - Choisissez une méthode d'optimisation.
   - Modifiez les paramètres de la barre, l'épaisseur de la lame, l'affranchissement, et la chute minimale si nécessaire.
   - Cliquez sur Lancer l'optimisation pour voir les résultats dans l'interface.
   - Cliquez sur Générer PDF pour créer un PDF avec les résultats et l'ouvrir automatiquement.

Génération de l'exécutable (.exe)

Vous pouvez utiliser PyInstaller pour créer un exécutable :

pyinstaller --onefile --windowed debitage_gui.py

L'exécutable sera créé dans le répertoire dist/.

Structure du projet

nom-du-repo/
│
├── debitage.py              # Fichier principal contenant les fonctions d'optimisation et de génération PDF
├── debitage_gui.py          # Interface graphique avec Tkinter
├── requirements.txt         # Fichier des dépendances
├── README.md                # Ce fichier
└── dist/                    # Répertoire où sera généré l'exécutable après l'utilisation de PyInstaller

Fonctionnalités futures

- Support de nouvelles méthodes d'optimisation.
- Option pour personnaliser davantage les rapports PDF (logo, couleurs, etc.).

Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou à créer des pull requests pour améliorer ce projet.

Licence

Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE pour plus d'informations.
