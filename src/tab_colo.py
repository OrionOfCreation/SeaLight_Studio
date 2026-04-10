# -*- coding: utf-8 -*-
# Copyright (c) 2025 OrionOfCreation
# Licensed under the MIT License - see LICENSE file for details
"""
Module de gestion de l'affichage colorimétrique.
Contient les fonctions permettant de tracer les données de chromaticité (X, Y)
et de superposer les zones limites réglementaires pour les différentes couleurs de feux.
"""


def trace_graph(data, ax):
    """
    Trace les points de données sur le graphique.

    Args:
        data (dict): Dictionnaire contenant les coordonnées 'X' et 'Y'.
        ax (matplotlib.axes.Axes): Axe matplotlib sur lequel tracer.
    """
    if data is None:
        return

    ax.clear()

    filtered_data = data[(data["cd"] >= 10)]

    # Tracer les données
    ax.scatter(filtered_data["X"], filtered_data["Y"], c="black", s=5, alpha=0.6)


def trace_limit(ax):
    """
    Trace les zones limites de couleur sur le diagramme chromatique.

    Args:
        ax (matplotlib.axes.Axes): Axe matplotlib sur lequel tracer les limites.
    """
    zone_white = {
        "X": [0.525, 0.525, 0.452, 0.310, 0.31, 0.443, 0.525],
        "Y": [0.382, 0.44, 0.44, 0.348, 0.283, 0.382, 0.382],
    }
    ax.plot(zone_white["X"], zone_white["Y"], color="grey", linestyle="--", alpha=0.5)

    zone_green = {
        "X": [0.028, 0.009, 0.3, 0.203, 0.028],
        "Y": [0.385, 0.723, 0.511, 0.356, 0.385],
    }
    ax.plot(zone_green["X"], zone_green["Y"], color="g", linestyle="--", alpha=0.5)
    ax.fill(zone_green["X"], zone_green["Y"], color="g", alpha=0.2)

    zone_red = {
        "X": [0.68, 0.66, 0.721, 0.735, 0.68],
        "Y": [0.32, 0.32, 0.259, 0.265, 0.32],
    }
    ax.plot(zone_red["X"], zone_red["Y"], color="r", linestyle="--", alpha=0.5)
    ax.fill(zone_red["X"], zone_red["Y"], color="r", alpha=0.2)

    zone_yellow = {
        "X": [0.612, 0.618, 0.575, 0.575, 0.612],
        "Y": [0.382, 0.382, 0.425, 0.406, 0.382],
    }
    ax.plot(zone_yellow["X"], zone_yellow["Y"], color="y", linestyle="--", alpha=0.5)
    ax.fill(zone_yellow["X"], zone_yellow["Y"], color="y", alpha=0.2)

    ax.set_title("Diagramme chromatique")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_xlim([0, 0.8])
    ax.set_ylim([0.2, 0.8])
    ax.minorticks_on()
    ax.grid(which="major", alpha=0.7)
    ax.grid(which="minor", linestyle="--", linewidth=0.5, alpha=0.4)
