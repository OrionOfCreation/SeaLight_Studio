# -*- coding: utf-8 -*-
# Copyright (c) 2025 OrionOfCreation
# Licensed under the MIT License - see LICENSE file for details
"""
Module de gestion de l'affichage photométrique.
Gère le traçage de l'intensité lumineuse en fonction de l'angle, l'application
de décalages angulaires et la visualisation des zones de conformité pour différents secteurs.
"""

import tkinter as tk
import zone as z


def trace_graph(data, ax, decalage, previous_line=None):
    """
    Trace le graphique de l'intensité lumineuse en appliquant un décalage angulaire.

    Args:
        data (pd.DataFrame): Données contenant les colonnes 'Angle °' et 'cd'.
        ax (matplotlib.axes.Axes): Axe matplotlib sur lequel tracer.
        decalage (tk.StringVar): Objet possédant une méthode get() pour obtenir le décalage.
        previous_line (matplotlib.lines.Line2D, optional): Ligne précédemment tracée à supprimer.

    Returns:
        matplotlib.lines.Line2D: L'objet ligne créé sur le graphique.
    """
    if data is None:
        return

    if previous_line is not None:
        previous_line.remove()

    try:
        val_decalage = eval(decalage.get())
    except NameError:
        tk.messagebox.showwarning(
            "Avertissement Wrong value", "Le décalage DOIT être une valeur chiffrée"
        )
        val_decalage = 0
    except SyntaxError:
        tk.messagebox.showwarning(
            "Avertissement WRONG VALUE",
            """Le décalage DOIT être une valeur chiffrée\n
 Vérifier si un caractère ne s'y est pas glissé""",
        )
        val_decalage = 0

    data["Angle °"] = data["Angle °"].apply(lambda x: x + val_decalage)

    # Tracer les données
    (line,) = ax.plot(data["Angle °"], data["cd"], color="steelblue")
    return line, val_decalage


def trace_limit(ax, secteur, range_val, inclinaison, boat_type, previous_limits=None):
    """
    Trace les zones limites (zones interdites) sur le graphique de photométrie.

    Args:
        ax (matplotlib.axes.Axes): Axe matplotlib sur lequel tracer les limites.
        secteur (str): Nom du secteur ("Hune", "Poupe", "Babord", "Tribord", "Vide").
        range_val (float): Valeur de la portée.
        inclinaison (float): Valeur de l'inclinaison.
        boat_type (str): indique si le bateau est à moteur ou à voile.
        previous_limits (list, optional): Liste des artistes précédemment tracés à supprimer.

    Returns:
        list: Liste des artistes matplotlib (lignes et remplissages) créés.
    """
    if previous_limits is not None:
        for artist in previous_limits:
            artist.remove()

    zone_interdite = {}
    if secteur == "Hune":
        zone_interdite = z.hune(range_val, inclinaison)
    elif secteur == "Poupe":
        zone_interdite = z.poupe(range_val, inclinaison)
    elif secteur == "Babord":
        zone_interdite = z.babord(range_val, inclinaison)
    elif secteur == "Tribord":
        zone_interdite = z.tribord(range_val, inclinaison)
    elif secteur == "180":
        zone_interdite = z.half_round(range_val, inclinaison)
    elif secteur == "360":
        zone_interdite = z.all_round(range_val, inclinaison)
    elif secteur == "Vide":
        zone_interdite = z.only_value()
    elif secteur == "Vertical":
        zone_interdite = z.vertical(range_val, boat_type)

    # Tracer les zones
    new_limits = []
    for zone_num in [1, 2, 3]:
        zone = zone_interdite[zone_num]
        limits_line = ax.plot(
            zone["X"], zone["Y"], color="red", linestyle="--", alpha=0.5
        )
        new_limits.extend(limits_line)
        limit_fill = ax.fill(
            zone["X"],
            zone["Y"],
            color="red",
            alpha=0.2,
        )
        new_limits.extend(limit_fill)

    ax.set_title("Intensité lumineuse en fonction de l'angle")
    ax.set_xlabel("Angle (°)")
    ax.set_ylabel("Intensité lumineuse (cd)")
    ax.minorticks_on()
    ax.grid(which="major", alpha=0.7)
    ax.grid(which="minor", linestyle="--", linewidth=0.5, alpha=0.4)
    ax.relim()
    ax.autoscale_view()
    return new_limits


def trace_factor(ax, data, secteur):
    """
    Calcule et trace le facteur d'intensité sur le secteur central.

    Le facteur est le ratio entre l'intensité maximale et minimale dans une zone
    spécifique définie par le secteur.

    Args:
        ax (matplotlib.axes.Axes): Axe matplotlib sur lequel tracer le point du facteur.
        data (pd.DataFrame): Données contenant les colonnes 'Angle °' et 'cd'.
        secteur (str): Nom du secteur ("Hune", "Poupe", "Babord" ou "Tribord").

    Returns:
        list: Liste des artistes matplotlib (point de dispersion et ligne horizontale) créés.
    """
    factor = 0.0
    zone_interdite = {}
    if secteur == "Hune":
        zone_interdite = z.hune()
    elif secteur == "Poupe":
        zone_interdite = z.poupe()
    elif secteur == "Babord":
        zone_interdite = z.babord()
    elif secteur == "Tribord":
        zone_interdite = z.tribord()
    elif secteur == "180":
        zone_interdite = z.half_round()
    elif secteur == "360":
        zone_interdite = z.all_round()
    elif secteur == "Vide":
        zone_interdite = z.only_value()
    elif secteur == "Vertical":
        zone_interdite = z.vertical()


    x_factor_l = int(zone_interdite[2]["X"][3])
    x_factor_r = int(zone_interdite[2]["X"][4])

    filtered_data = data[
        (data["Angle °"] >= x_factor_l) & (data["Angle °"] <= x_factor_r)
    ]

    factor_graph = []
    if not filtered_data.empty:
        min_row = filtered_data.loc[filtered_data["cd"].idxmin()]
        max_row = filtered_data.loc[filtered_data["cd"].idxmax()]
        factor = round(max_row["cd"] / min_row["cd"], 2)

        factor_point_min = ax.scatter(
            x=min_row["Angle °"],
            y=min_row["cd"],
            c="r",
            label=f"facteur d'intensité: {factor}",
            s=10,
            zorder=3,
            edgecolors="darkred",
            linewidths=1.5,
        )
        factor_graph.append(factor_point_min)

        factor_point_max = ax.scatter(
            x=max_row["Angle °"],
            y=max_row["cd"],
            c="r",
            s=10,
            zorder=3,
            edgecolors="darkred",
            linewidths=1.5,
        )
        factor_graph.append(factor_point_max)

        factor_line = ax.axhline(
            y=min_row["cd"] * 1.5,
            color="r",
            linestyle="-.",
            linewidth=1.5,
            zorder=2,
        )
        factor_graph.append(factor_line)

    else:
        return None

    return factor_graph
