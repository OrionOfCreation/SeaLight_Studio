# -*- coding: utf-8 -*-
# Copyright (c) 2025 OrionOfCreation
# Licensed under the MIT License - see LICENSE file for details
"""
Module de calcul des zones d'intensité et des coordonnées géométriques.
Définit les limites d'intensité lumineuse et les secteurs angulaires pour les différents
types de feux de navigation (Hune, Poupe, Babord, Tribord) selon les normes.
"""

import tkinter as tk

def max_power(light_range, inclinaison):
    """
    Calcule la puissance maximale basée sur la portée de la lumière et l'inclinaison,

    Args:
        light_range (int): La portée de la lumière (1-6).
        inclinaison (float/int): L'angle d'inclinaison. Si non nul, puissance est divisée par deux.

    Returns:
        int : valeur maximal de l'intensité
    """

    max = 0
    match light_range:
        # Valeur tirée de la norme USCG/ABYC-C5
        case 1:
            max = 1.1
        case 2:
            max = 5.4
        case 3:
            max = 15
        case 4:
            max = 33
        case 5:
            max = 65
        case 6:
            max = 118
        case _:
            tk.messagebox.showwarning("Avertissement: No range", "choisir une portée.")
            return

    if inclinaison != 0:
        max *= 0.5  # if not 0°, divide power riquiered by 2

    return max

def intensity_calc(light_range, inclinaison):
    """
    Retourne un dictionnaire de valeurs d'intensité pour trois zones.

    Args:
        light_range (int): La portée de la lumière (1-6).
        inclinaison (float/int): L'angle d'inclinaison. Si non nul, puissance est divisée par deux.

    Returns:
        dict: Un dictionnaire contenant les données
        d'intensité (valeurs Y) pour les zones 1, 2 et 3.
    """

    max_intesity = max_power(light_range, inclinaison)
    return {
        # define 3 no-go zone
        1: {
            "Y": [  # have to go under 10% of the max power
                0.1 * max_intesity,
                max_intesity,
                max_intesity,
                0.1 * max_intesity,
                0.1 * max_intesity,
            ]
        },
        2: {
            "Y": [  # may have 5 degrees of half power (e.g. masthead or stern)
                0,
                0.5 * max_intesity,
                0.5 * max_intesity,
                max_intesity,
                max_intesity,
                0.5 * max_intesity,
                0.5 * max_intesity,
                0,
                0,
            ]
        },
        3: {"Y": [max_intesity, 0.1 * max_intesity, 0.1 * max_intesity, max_intesity, max_intesity]},
    }


def hune(light_range=1, inclinaison=0):
    """
    Définit les coordonnées pour les zones interdites d'un feux de hune.

    Args:
        light_range (int): La portée de la lumière.
        inclinaison (float/int): L'angle d'inclinaison.

    Returns:
        dict: Le dictionnaire d'intensité avec les coordonnées X ajoutées pour chaque zone.
    """
    zone = intensity_calc(light_range, inclinaison)

    # angle hune donné par USCG/ABYC-C5
    zone[1]["X"] = [-132.5, -132.5, -117.5, -117.5, -132.5]
    zone[2]["X"] = [-112.5, -112.5, -107.5, -107.5, 107.5, 107.5, 112.5, 112.5, -112.5]
    zone[3]["X"] = [132.5, 132.5, 117.5, 117.5, 132.5]

    return zone


def poupe(light_range=1, inclinaison=0):
    """
    Définit les coordonnées pour les zones interdite d'un feu de poupe.

    Args:
        light_range (int): La portée de la lumière.
        inclinaison (float/int): L'angle d'inclinaison.

    Returns:
        dict: Le dictionnaire d'intensité avec les coordonnées X ajoutées pour chaque zone.
    """
    zone = intensity_calc(light_range, inclinaison)

    # angle poupe donné par USCG/ABYC-C5
    zone[1]["X"] = [85, 85, 107.5, 107.5, 85]
    zone[2]["X"] = [112.5, 112.5, 117.5, 117.5, 242.5, 242.5, 247.5, 247.5, 112.5]
    zone[3]["X"] = [267.5, 267.5, 252.5, 252.5, 267.5]

    return zone


def babord(light_range=1, inclinaison=0):
    """
    Définit les coordonnées pour les zones interdite d'un feu bâbord.

    Args:
        light_range (int): La portée de la lumière.
        inclinaison (float/int): L'angle d'inclinaison.

    Returns:
        dict: Le dictionnaire d'intensité avec les coordonnées X ajoutées pour chaque zone.
    """
    zone = intensity_calc(light_range, inclinaison)

    # angle babord donné par USCG/ABYC-C5
    zone[1]["X"] = [-30, -30, -3, -3, -30]
    zone[2]["X"] = [0, 0, 0, 0, 107.5, 107.5, 112.5, 112.5, 0]
    zone[3]["X"] = [142.5, 142.5, 117.5, 117.5, 142.5]

    return zone


def tribord(light_range=1, inclinaison=0):
    """
    Définit les coordonnées pour les zones interdite d'un feu tribord.

    Args:
        light_range (int): La portée de la lumière.
        inclinaison (float/int): L'angle d'inclinaison.

    Returns:
        dict: Le dictionnaire d'intensité avec les coordonnées X ajoutées pour chaque zone.
    """
    zone = intensity_calc(light_range, inclinaison)

    # angle tribord donné par USCG/ABYC-C5
    zone[1]["X"] = [-142.5, -142.5, -117.5, -117.5, -142.5]
    zone[2]["X"] = [-112.5, -112.5, -107.5, -107.5, 0, 0, 0, 0, -112.5]
    zone[3]["X"] = [30, 30, 3, 3, 30]

    return zone


def all_round(light_range=1, inclinaison=0):
    """
    Définit les coordonnées pour les zones interdite d'un feu de 360°.

    Args:
        light_range (int): La portée de la lumière.
        inclinaison (float/int): L'angle d'inclinaison.

    Returns:
        dict: Le dictionnaire d'intensité avec les coordonnées X ajoutées pour chaque zone.
    """
    zone = intensity_calc(light_range, inclinaison)

    # rectangle de 0 à 360
    zone[1]["X"] = [0, 0, 0, 0, 0]
    zone[2]["X"] = [0, 0, 0, 0, 360, 360, 360, 360, 0]
    zone[3]["X"] = [360, 360, 360, 360, 360]

    return zone


def half_round (light_range=1, inclinaison=0):
    """
    Définit les coordonnées pour les zones interdite d'un feu de 180° à tribord.

    Args:
        light_range (int): La portée de la lumière.
        inclinaison (float/int): L'angle d'inclinaison.

    Returns:
        dict: Le dictionnaire d'intensité avec les coordonnées X ajoutées pour chaque zone.
    """
    zone = intensity_calc(light_range, inclinaison)

    # angle tribord donné par USCG/ABYC-C5
    zone[1]["X"] = [-30, -30, -3, -3, -30]
    zone[2]["X"] = [0, 0, 5, 5, 175, 175, 180, 180, 0]
    zone[3]["X"] = [185, 185, 210, 210, 185]

    return zone


def only_value():
    """
    Retourne un dictionnaire de zone avec des coordonnées initialisées à zéro.

    Returns:
        dict: Une structure de dictionnaire pour trois zones avec des valeurs X et Y vides ou nulles
    """
    zone = {}
    zone[1] = {"X": [], "Y": []}
    zone[2] = {"X": [], "Y": []}
    zone[3] = {"X": [], "Y": []}

    zone[1]["X"] = [0]
    zone[1]["Y"] = [0]
    zone[2]["X"] = [0]
    zone[2]["Y"] = [0]
    zone[3]["X"] = [0]
    zone[3]["Y"] = [0]

    return zone


def vertical (light_range=1, boat_type="motor"):
    """
    Définit les coordonnées pour les zones interdite d'un feu lors du test vertical.

    Args:
        light_range (int): La portée de la lumière (1-6).
        boat_type (str): indique le type de bateau (moteur ou voile)

    Returns:
        dict: Le dictionnaire d'intensité des zones interdites.
    """

    zone = {1: {}, 2: {}, 3: {}}
    intensity_max = max_power(light_range,0)

    if boat_type == "motor":
        zone[1]["Y"] = [0, 0, 0, 0, 0]
        zone[2]["Y"] = [0, 0.6*intensity_max, 0.6*intensity_max, intensity_max, intensity_max, 0.6*intensity_max, 0.6*intensity_max, 0, 0]
        zone[3]["Y"] = [0, 0, 0, 0, 0]

        zone[1]["X"] = [0, 0, 0, 0, 0]
        zone[2]["X"] = [-7.5, -7.5, -5, -5, 5, 5, 7.5, 7.5, -7.5]
        zone[3]["X"] = [0, 0, 0, 0, 0]

    elif boat_type == "sail":
        zone[1]["Y"] = [0, 0, 0, 0, 0]
        zone[2]["Y"] = [0, 0.5*intensity_max, 0.5*intensity_max, intensity_max, intensity_max, 0.5*intensity_max, 0.5*intensity_max, 0, 0]
        zone[3]["Y"] = [0, 0, 0, 0, 0]

        zone[1]["X"] = [0, 0, 0, 0, 0]
        zone[2]["X"] = [-25, -25, -5, -5, 5, 5, 25, 25, -25]
        zone[3]["X"] = [0, 0, 0, 0, 0]

    return zone
