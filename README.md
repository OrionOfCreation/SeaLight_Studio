# Analyseur de Feux de Navigation - SeaLight_Studio

Application d'analyse des données photométriques et colorimétriques pour les feux de navigation maritime conformes aux normes Wheelmark et USCG/ABYC-C5.

[![iso](https://img.shields.io/badge/LA-RACHE-blue.svg "ISO 1664")](https://www.la-rache.com/presentation.html)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

<img src="icon/splash_screen.png">


## Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Format des données](#format-des-données)
- [Normes et références](#normes-et-références)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Aperçu

Cette application permet d'analyser et de valider la conformité des feux de navigation maritime en traçant :
- **Courbes photométriques** : Intensité lumineuse (cd) en fonction de l'angle
- **Diagrammes colorimétriques** : Coordonnées chromatiques (X, Y) sur le diagramme CIE

L'outil aide à la vérification de la conformité avec les zones réglementaires pour différents types de feux :
- Feu de hune (masthead)
- Feu de poupe (stern)
- Feu de bâbord (port)
- Feu de tribord (starboard)

## Fonctionnalités

### Analyse photométrique
- Tracé de l'intensité lumineuse en fonction de l'angle
- Application de décalages angulaires
- Visualisation des zones de conformité selon le secteur
- Calcul du facteur d'intensité (ratio max/min × 1.5)
- Support des inclinaisons 0° et ±25° (±5° assimilé à 0°)
- Portées de 1 à 6 miles nautiques

### Analyse colorimétrique
- Diagramme de chromaticité CIE (X, Y)
- Zones réglementaires pour :
  - Blanc (white)
  - Vert (green)
  - Rouge (red)
  - Jaune (yellow)

## Installation

Si vous souhaitez juste utiliser l'application une version est disponible dans les [releases](https://github.com/OrionOfCreation/SeaLight_Studio/releases)  
Si par contre votre souhait est d'utiliser les fichiers sources, les étapes à suivres sont ci-dessous.

### Prérequis

- Python 3.12.3 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation du projet

1. Clonez ou téléchargez le projet :
```bash
git clone https://github.com/Auguitare/SeaLight_Studio.git
cd SeaLight_Studio
```

2. Installez les bibliothèques nécessaires :
```bash
sudo apt install python3.12-venv
```

3. Créez l'environement
```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Installez les dépendances :
un fichier [requierment.txt](/requirements.txt) est disponible
```bash
pip install -r requirements.txt
```

5. Lancez l'application :
```bash
python src/main.py
```

6. Creez une application portable

    Il est pssible d'utiliser le code sur une application portable de 2 manières différentes :
    - Soit en la compilant par cous même et pour cela veuilliez consultez le fichier [instruction.md](/instruction.md) pour connaitre les paramètres 
    - Soit en la téléchargant depuis la dernière release directement sur [github](https://github.com/Auguitare/SeaLight_Studio/releases)

## Utilisation 

### Lancement rapide

1. **Démarrez l'application** :
    - Via l'application télécharger dans les [releases github](https://github.com/Auguitare/SeaLight_Studio/releases) (colonne de droite de la page)
    - Via les fichiers sources:
        ```bash
        source .venv/bin/activate
        python main.py
        ```

2. **Choisissez un fichier de données** :
    - Cliquez sur "Choisir un fichier" (Ctrl+O)
    - Sélectionnez votre fichier (CSV ou TXT)

3. **Configurez les paramètres** (uniquement onglet Photométrie) :
    - Secteur : Hune, Poupe, Bâbord, Tribord ou Vide (sans zone limite tracée)
    - Portée : 1 à 6 miles nautiques
    - Inclinaison du test  : 0° ou ±25°
        > [!NOTE]  
        > Les tests à ±5° ont les même contrainte qu'à 0°, choisissez donc 0°.

4. **Tracez le graphique** :
    - Cliquez sur "Tracer le graphique" (ou appuyez sur Entrée)

5. **Ajustez la position de votre graphique**
    - Utilisez l'entrée "Décalage [°]" pour ajuster la position de votre graphique dans les bornes des secteurs
        > [!NOTE]
        > Le décalage est une valeur chiffré mais est aussi modifiable via les flèches directionnelles: haut/bas pour un pas de 1° et gauche/droite pour un pas précis de 0.2°

6. **Ajustement visuel**
    - Ajustez si besoin le zoom et la position du graphique avec la toolbar en dessous 

7. **Sauvegardez**
    - Sauvegardez votre graphique avec la dernière icone de la toolbar

### Guide détaillé

#### <u>Onglet Photométrie</u>

**Paramètres disponibles :**

| Paramètre | Description | Valeurs |
|-----------|-------------|---------|
| Secteur | Type de feu à analyser | Hune, Poupe, Bâbord, Tribord, Vide, 360°, 180° babord et tribord |
| Portée | Distance en miles nautiques | 1, 2, 3, 4, 5, 6 |
| Inclinaison | Angle d'inclinaison du test | 0°, ±25° |
| Décalage | Correction angulaire (en degrés) | Valeur décimale |
| Facteur 1.5 | Affiche le facteur d'intensité | Checkbox |

**Lecture du graphique :**
- **Courbe bleue** : Intensité mesurée
- **Zones rouges** : Zones interdites (non-conformité)
- **Point rouge** (si facteur activé) : Intensité minimale et maximale dans la zone
- **Ligne rouge pointillée** : Seuil du facteur 1.5

#### <u> Onglet Colorimétrie</u>

Affiche le diagramme chromatique avec :
- **Points noirs** : Mesures de votre feu
- **Zones colorées** : Zones réglementaires pour chaque couleur

Les points doivent se situer dans la zone correspondant à la couleur du feu.

### Raccourcis clavier

- `Entrée`  : Tracer le graphique de l'onglet actif (marche aussi avec le Keyboard)
- `Ctrl+O`  : Ouvrir un fichier
- `Ctrl+F`  : Toggle du facteur d'intensité
- `Ctrl+Tab`: Changer d'onglet
- `R`: Réinitialiser le graphe
- `Flèche direction Gauche\Droite` : +/- 0.2° au décalage
- `Flèche direction Haut\Bas` : +/- 1° au décalage
- `Ctrl+Q`  : Quittez l'application

## Structure du projet

```
SeaLight_Studio/
├
├──src/
    ├── main.py              # Application principale
    ├── tab_photo.py         # Affichage onglet photométrique
    ├── tab_colo.py          # Affichage onglet colorimétrique
    ├── zone.py              # Calculs des zones de conformité
    ├── file_orga.py         # Gestion des fichiers
├
├──icon/
    ├── icon.ico             # Icône Windows (optionnel)
    ├── icon.png             # Icône UNIX (optionnel)
    ├── splash_screen.png    # Imagede démarrage
├
├──rapid_test_file           # fichier pour test et debug
    ├── babord_limit_boundaries.txt
    ├── hune_valide.txt
    ├── poupe.txt
    ├── test_colo.txt
    ├── test.txt
    ├── tribord_180.txt
    ├── unvalid_test.txt
├
├──.github/workflows/
    ├── build.yml            # Fichier d'automatisation
├
├──archive/                  # Dossier d'anciens fichiers  
├
├──image_README/             # Image nécessaire pour le README  
├
├──patch/                    # Fichiers de conseil
├
├── README.md                # Ce fichier
├── instruction.md           # Instruction PyInstaller
├── LICENCE                  # Licence MIT
└── requirements.txt         # Liste des dépendances
```

### Description des fichiers

#### `main.py`
Point d'entrée de l'application. Gère :
- Interface utilisateur (fenêtre, onglets, boutons)
- Coordination entre les différents modules
- Gestion des événements utilisateur

#### `tab_photo.py`
Module de photométrie. Fonctions principales :
- `trace_graph()` : Trace la courbe d'intensité
- `trace_limit()` : Affiche les zones réglementaires
- `trace_factor()` : Calcule et affiche le facteur d'intensité

#### `tab_colo.py`
Module de colorimétrie. Fonctions principales :
- `trace_graph()` : Trace les points chromatiques
- `trace_limit()` : Affiche les zones de couleur réglementaires

#### `zone.py`
Calculs des zones de conformité. Fonctions :
- `intensity_calc()` : Calcule les intensités limites
- `hune()`, `poupe()`, `babord()`, `tribord()` : Définit les coordonnées des zones

#### `file_orga.py`
Gestion des fichiers. Fonctions :
- `choisir_fichier()` : Dialogue de sélection de fichier
- `read_file()` : Lecture et parsing des données

#### `theme.json`
fichier esthétique de l'application.

#### `build.yml`
Gère l'automatisation de la compilation et des releases

## Format des données

### Format CSV/TXT attendu

Le fichier doit contenir une ligne d'en-tête avec le mot "Angle" suivie des données :

```csv
Angle °;cd;lux;X;Y
-180.0;0.52;0.12;0.315;0.330
-179.0;0.54;0.13;0.316;0.331
...
```

**Colonnes requises :**
- `Angle °` : Angle de mesure (en degrés)
- `cd` : Intensité lumineuse (en candelas)
- `lux` : Éclairement (en lux)
- `X` : Coordonnée chromatique X (CIE 1931)
- `Y` : Coordonnée chromatique Y (CIE 1931)

**Format du fichier :**
- Séparateur : point-virgule (`;`)
- Encodage : UTF-8
- Les deux dernières lignes sont ignorées

### Exemple de fichier

```
Informations du test
Date: 2024-02-07
Équipement: Feu de navigation LED
---
Angle °;cd;lux;X;Y
0.0;5.8;1.35;0.320;0.335
1.0;5.7;1.33;0.321;0.336
2.0;5.6;1.30;0.319;0.334
...
Notes complémentaires
Fin du fichier
```

## Normes et références

### Normes appliquées
<img src="image_README/USCG.png" width="400">
<img src="image_README/ABYC.png" width="400">
<img src="image_README/wheelmark.png" width="400">

- **USCG (United States Coast Guard) ABYC-C5** : American Boat & Yacht Council - Standard C5
- **Wheelmark** : Certification européen pour les équipements maritimes
- **EN 14744** : Norme technique européenne pour les feux de navigation

### Portées et intensités

| Portée (NM) | Intensité minimale (cd) à 0° | Intensité minimale (cd) à ±25° |
|-------------|------------------------------|--------------------------------|
| 1           | 1.1                          | 0.55                           |
| 2           | 5.4                          | 2.7                            |
| 3           | 15                           | 7.5                            |
| 4           | 33                           | 16.5                           |
| 5           | 65                           | 32.5                           |
| 6           | 118                          | 59                             |

### Secteurs angulaires

| Type de feu | Secteur horizontal
|-------------| -----
| Hune        | 225° (112.5° B/T) vers l'avant
| Poupe       | 135° (67.5° B/T) vers l'arrière
| Bâbord      | 112.5° (vers B)
| 180 Babord  | 180°   (vers B)
| Tribord     | 112.5° (vers T)
| 180 Tribord | 180°   (vers T)
| 360         | 360°

### Couleurs réglementaires (coordonnées CIE)

**Blanc :**
- X: 0.310 - 0.525
- Y: 0.283 - 0.440

**Vert :**
- X: 0.009 - 0.300
- Y: 0.356 - 0.723

**Rouge :**
- X: 0.660 - 0.735
- Y: 0.259 - 0.320

**Jaune :**
- X: 0.575 - 0.618
- Y: 0.382 - 0.425

## Dépannage

### L'application ne se lance pas

<u> ***ATTENDEZ !*** </u>  : Si vous avez lancer le fichier de la release, l'application peut mettre un peu de temps a démarrer. C'est le prix à payer pour avoir une application en un seul fichier. 

Si vous lancer les code source:

**Problème** : `ModuleNotFoundError: No module named 'customtkinter'` (par exemple)

**Solution** :
```bash
pip install -r requirements.txt
```
ou
```bash
pip install customtkinter
```

### Erreur lors du chargement du fichier

**Problème** : "Colonnes manquantes dans le fichier"

**Solution** :
- Vérifiez que votre fichier contient bien les colonnes : `Angle °`, `cd`, `lux`, `X`, `Y`
- Vérifiez que le séparateur est bien un point-virgule (`;`)

### Les zones ne s'affichent pas correctement

**Problème** : Zones rouges absentes, mal positionnées ou de mauvaise amplitude.

**Solution** :
- Vérifiez que vous avez sélectionné un secteur (pas "Vide") et que c'est celui que vous souhaitez
- Vérifiez que la portée est bien configurée (1-6)
- Vérifier le décalage de votre graphe
- Retracer le graphe avec "Tracer le graphique"

### Autres problèmes

N'hesitez pas a rapporter les erreurs que vous n'arrivez pas à résoudre via les issues github

## Contribuer

Les contributions sont les bienvenues !

### Axes d'amélioration possible

- [x] Géré  les feux non normé (360° et 180°)
- [x] Modifier les couleurs/visuel de l'app
- [x] ajouter raccourcis
  - [x] Ajouter Tab pour changer d'onglet
  - [x] Ajouter flèche de direction pour augmenter le décalage
  - [x] Ctrl+f pour toggle le facteur d'intensité
- [x] automatisation de PyInstaller (via runner github)
- [x] ajouter bouton mode clair/sombre
- [ ] Comparaison entre plusieurs feux
- [ ] ~~Mode batch pour analyser plusieurs fichiers~~ => same as juste above
- [ ] ~~Export des résultats en PDF~~ => export des graphe en PNG
- [ ] Génération de rapports de conformité

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](/LICENSE) pour plus de détails.

## Auteur

Développé avec ❤️ (et python) pour l'analyse de conformité des feux de navigation maritime.

## Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation des normes USCG/ABYC-C5 ou de la Wheelmark

---

> [!CAUTION]
> Cette application est un outil d'aide à l'analyse. Les résultats doivent être validés par un organisme certifié pour une homologation officielle.
