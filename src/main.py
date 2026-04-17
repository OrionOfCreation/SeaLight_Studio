# -*- coding: utf-8 -*-
# Copyright (c) 2025 OrionOfCreation
# Licensed under the MIT License - see LICENSE file for details
"""
Script principal de l'application d'analyse des données photométriques et colorimétriques.
Ce module initialise l'interface utilisateur avec customtkinter, gère les onglets de navigation,
le chargement des fichiers de données et coordonne l'affichage des graphiques.
"""

import platform
import tkinter as tk

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import file_orga as orga
import tab_photo as photo_file
import tab_colo as colo_file

# Source - https://stackoverflow.com/a/79340292
# Posted by asmaier
# Retrieved 2026-03-10, License - CC BY-SA 4.0
try:
    import pyi_splash

    pyi_splash.close()
except:
    pass

_GRAPH_THEMES = {
    "dark": {
        "bg":     "#0D1B2A",
        "axes":   "#162032",
        "text":   "#CAD8E8",
        "spine":  "#1E3A5F",
        "grid":   "#1E3A5F",
    },
    "light": {
        "bg":     "#F0F4F8",
        "axes":   "#FFFFFF",
        "text":   "#1A2B3C",
        "spine":  "#879AA8",
        "grid":   "#879AA8",
    },
}

def _apply_ax_theme(fig, ax, theme_key):
    """Applique un thème clair/sombre à une figure et son axe matplotlib."""
    t = _GRAPH_THEMES[theme_key]
    fig.set_facecolor(t["bg"])
    ax.set_facecolor(t["axes"])
    ax.tick_params(colors=t["text"])
    ax.xaxis.label.set_color(t["text"])
    ax.yaxis.label.set_color(t["text"])
    ax.title.set_color(t["text"])
    for spine in ax.spines.values():
        spine.set_edgecolor(t["spine"])
    ax.grid(color=t["grid"])


class Application(ctk.CTk):
    """
    Classe principale de l'application.\n
    Gère l'interface utilisateur, le chargement des fichiers et l'affichage des graphiques.
    """

    def __init__(self):
        """
        Initialise la fenêtre principale, les onglets et les éléments de l'UI.
        """
        super().__init__()

        self.file_chosen = None
        self.data = None
        self.intensity_factor = None
        self.current_photo_line = None
        self.current_photo_limits = []

        self._setup_window()
        self._setup_tabs()
        self._setup_photometry_tab()
        self._setup_colorimetry_tab()
        self._setup_keybindings()

        # Live update
        self._live_active = False
        self._live_job = None


        # --- Barre de Menu ---
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # -- Menu Fichier --
        self.menu_fichier = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menu_fichier.add_command(
            label="Ouvrir un fichier...",
            command=self.file,
            accelerator="Ctrl+O",
        )
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(
            label="Quitter", command=self.quit, accelerator="Ctrl+Q"
        )

        # -- Menu Affichage (Thèmes) --
        self.menu_affichage = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Affichage", menu=self.menu_affichage)

        self.menu_affichage.add_radiobutton(
            label="Mode Sombre",
            command=lambda: self.changer_theme("Dark"),
        )
        self.menu_affichage.add_radiobutton(
            label="Mode Clair",
            command=lambda: self.changer_theme("Light"),
        )
        self.menu_affichage.add_radiobutton(
            label="Système",
            command=lambda: self.changer_theme("System"),
        )

        # -- Menu Aide --
        self.menu_aide = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Aide", menu=self.menu_aide)
        self.menu_aide.add_command(label="À propos", command=self.a_propos)

    def _setup_window(self):
        """Configure la fenêtre principale"""
        self.title("Analyse des données photométrique des feux de navigation")
        self.geometry("800x600")

        # ctk.set_appearance_mode("light")
        theme_path = orga.resource_path("src/theme.json")
        ctk.set_default_color_theme(theme_path)

        try:
            if platform.system() == "Windows":
                icon_path = orga.resource_path("icon/icon.ico")
                self.iconbitmap(icon_path)
            else:
                icon_path = orga.resource_path("icon/icon.png")
                icon = tk.PhotoImage(file=icon_path)
                self.iconphoto(False, icon)
        except tk.TclError as e:
            print(f"Impossible de charger l'icône: {e}")

    def _setup_tabs(self):
        """Crée les onglets"""
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=0, pady=0, fill="both", expand=True)
        self.tabview.add("Photométrie")
        self.tabview.add("Colorimétrie")
        self.tabview.set("Photométrie")

    def _setup_photometry_tab(self):
        """Configure l'onglet photométrie"""
        tab_photo = self.tabview.tab("Photométrie")

        # Configuration de la grille
        tab_photo.grid_rowconfigure(0, weight=0)
        tab_photo.grid_rowconfigure(1, weight=0)
        tab_photo.grid_rowconfigure(2, weight=0)
        tab_photo.grid_rowconfigure(3, weight=1)
        tab_photo.grid_columnconfigure(0, weight=1)
        tab_photo.grid_columnconfigure(1, weight=2)
        tab_photo.grid_columnconfigure(2, weight=0)

        # Variable de la page
        self.var_secteur = ctk.StringVar(value="Vide")
        self.var_range = ctk.StringVar(value="3")
        self.var_angle = ctk.IntVar(value=0)
        self.var_boat_type = ctk.StringVar(value="motor")
        self.var_decalage = ctk.StringVar(value="0.0")
        self.var_intensity_factor = ctk.BooleanVar(value=False)

        # ===== Gestion des bouton/menu =====
        # position du feux
        secteur_menu = ctk.CTkOptionMenu(
            tab_photo,
            values=[
                "Vide",
                "Hune",
                "Poupe",
                "Babord",
                "Tribord",
                "180",
                "360",
                "Vertical",
            ],
            variable=self.var_secteur,
            anchor = "center",
        )
        secteur_menu.grid(row=1, column=0, padx=(10,0), pady=5, sticky="w")

        # Puissance du feux
        range_label = ctk.CTkLabel(tab_photo, text="Range [NM] :")
        range_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        range_menu = ctk.CTkOptionMenu(
            tab_photo,
            values=["1", "2", "3", "4", "5", "6"],
            variable=self.var_range,
            width=50,
        )
        range_menu.grid(row=2, column=0, padx=(100,0), pady=5, sticky="w")

        # Radio bouton d'angle
        rb_0 = ctk.CTkRadioButton(
            tab_photo, text="0°", variable=self.var_angle, value=0
        )
        rb_25 = ctk.CTkRadioButton(
            tab_photo, text="+/-25°", variable=self.var_angle, value=25
        )
        rb_0.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        rb_25.grid(row=2, column=1, padx=(150,10), pady=5, sticky="w")

        # Radio bouton de secteurs verticaux
        rb_motor = ctk.CTkRadioButton(
            tab_photo, text="Motorboat", variable=self.var_boat_type, value="motor"
        )
        rb_sail = ctk.CTkRadioButton(
            tab_photo, text="Sailboat", variable=self.var_boat_type, value="sail", width=150
        )
        rb_motor.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        rb_sail.grid(row=1, column=1, padx=(150,10), pady=5, sticky="w")

        # Bouton de choix de fichier
        button_fichier = ctk.CTkButton(
            tab_photo, text="Choisir un fichier", command=self.file
        )
        button_fichier.grid(row=0, column=0, padx=(10,0), pady=5, sticky="w")
        self.label_fichier_photo = ctk.CTkLabel(
            tab_photo, text="Aucun fichier sélectionné"
        )
        self.label_fichier_photo.grid(
            row=0, column=1, columnspan=2, padx=(10,10), pady=5, sticky="w"
        )

        # Entrée de decalage
        entry_decalage = ctk.CTkEntry(
            tab_photo, textvariable=self.var_decalage, width=50
        )
        entry_decalage.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        label_decalage = ctk.CTkLabel(tab_photo, text="Décalage [°]:")
        label_decalage.grid(row=0, column=2, padx=(10, 65), pady=5, sticky="e")

        # checkbox facteur 1.5
        self.checkbox_intensity_factor = ctk.CTkCheckBox(
            tab_photo,
            text="Facteur d'intensité 1.5",
            variable=self.var_intensity_factor,
            command=self.trace_intensity_factor,
        )
        self.checkbox_intensity_factor.grid(
            row=1, column=2, padx=(45, 10), pady=5, sticky="e"
        )

        # Bouton de traçage de graphique
        button_trace_photo = ctk.CTkButton(
            tab_photo, text="Tracer le graphique", command=self.trace_photo
        )
        button_trace_photo.grid(row=2, column=2, padx=(10,10), pady=5, sticky="e")

        #live update button
        self.button_live = ctk.CTkButton(
            tab_photo,
            text="▶ Live",
            width=60,
            command=self._toggle_live_update,
        )
        self.button_live.grid(row=2, column=2, padx=(10,160), pady=5, sticky="e")

        # == GRAPHIQUE PHOTOMÉTRIE ==
        self.frame_graph_photo = ctk.CTkFrame(tab_photo)
        self.frame_graph_photo.grid(
            row=3, column=0, columnspan=3, padx=0, pady=0, sticky="nsew"
        )

        # figure matplotlib
        self.fig_photo = Figure(figsize=(8, 5))
        self.ax_photo = self.fig_photo.add_subplot(111)
        self.current_photo_limits = photo_file.trace_limit(
            self.ax_photo,
            self.var_secteur.get(),
            int(self.var_range.get()),
            self.var_angle.get(),
            self.current_photo_limits,
        )

        # Intégration
        self.canvas_photo = FigureCanvasTkAgg(
            self.fig_photo, master=self.frame_graph_photo
        )

        # ajout de la toolbar
        toolbar = NavigationToolbar2Tk(self.canvas_photo, self.frame_graph_photo)
        toolbar.update()

        # gestion de la taille des élément du canva
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas_photo.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig_photo.tight_layout()
        self.canvas_photo.draw()

    def _setup_colorimetry_tab(self):
        """Configure l'onglet colorimétrie"""
        tab_color = self.tabview.tab("Colorimétrie")

        # Configuration de la grille
        tab_color.grid_rowconfigure(0, weight=0)
        tab_color.grid_rowconfigure(1, weight=0)
        tab_color.grid_rowconfigure(2, weight=1)
        tab_color.grid_columnconfigure(0, weight=1)
        tab_color.grid_columnconfigure(1, weight=1)
        tab_color.grid_columnconfigure(2, weight=1)

        # === Ligne 0 ===
        label_info = ctk.CTkLabel(
            tab_color,
            text="Colorimétrie - Diagramme de chromaticité (X, Y)",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        label_info.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        # === Ligne 1 ===
        button_fichier = ctk.CTkButton(
            tab_color, text="Choisir un fichier", command=self.file
        )
        button_fichier.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.label_fichier_color = ctk.CTkLabel(
            tab_color, text="Aucun fichier sélectionné"
        )
        self.label_fichier_color.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        button_trace_color = ctk.CTkButton(
            tab_color, text="Tracer le graphique", command=self.trace_color
        )
        button_trace_color.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        # == GRAPHIQUE Colorimétrie ==
        self.frame_graph_color = ctk.CTkFrame(tab_color)
        self.frame_graph_color.grid(
            row=2, column=0, columnspan=3, padx=0, pady=0, sticky="nsew"
        )

        # figure matplotlib
        self.fig_color = Figure(figsize=(8, 5))

        self.ax_color = self.fig_color.add_subplot(111)
        colo_file.trace_limit(self.ax_color)

        # Intégration
        self.canvas_color = FigureCanvasTkAgg(
            self.fig_color, master=self.frame_graph_color
        )

        # ajout toolbar
        toolbar = NavigationToolbar2Tk(self.canvas_color, self.frame_graph_color)
        toolbar.update()

        self.canvas_color.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.fig_photo.tight_layout()
        self.canvas_color.draw()

    def _setup_keybindings(self):
        """Configure les raccourcis clavier"""
        self.bind("<Return>", self.enter_handel)
        self.bind("<KP_Enter>", self.enter_handel)
        self.bind("<Control-o>", self.file)
        self.bind("<Control-f>", self.checkbox_intensity_factor.toggle)
        self.bind("<Control-Tab>", self.switch_tab)
        self.bind("<Left>", self.decal_handle)
        self.bind("<Right>", self.decal_handle)
        self.bind("<Up>", self.decal_handle)
        self.bind("<Down>", self.decal_handle)
        self.bind("r", self.resize_handle)
        self.bind("<Control-q>", lambda e: self.quit())

    def _file_loaded(self):
        """
        Vérifie qu'un fichier est sélectionné.

        Returns:
            bool: True si un fichier est chargé, False sinon (affiche un warning)
        """
        if not self.file_chosen:
            tk.messagebox.showwarning(
                "Avertissement: No File", "Veuillez d'abord choisir un fichier à ouvrir."
            )
            return False
        return True

    def trace_photo(self):
        """
        Lit les données du fichier sélectionné et trace le graphique de photométrie.
        Affiche un avertissement si aucun fichier n'est sélectionné.
        """
        if not self._file_loaded():
            return

        self.data = orga.read_file(self.file_chosen)
        self.current_photo_line, decal_update = photo_file.trace_graph(
            self.data, self.ax_photo, self.var_decalage, self.current_photo_line
        )
        self.var_decalage.set(decal_update)
        self.current_photo_limits = photo_file.trace_limit(
            self.ax_photo,
            self.var_secteur.get(),
            int(self.var_range.get()),
            self.var_angle.get(),
            self.var_boat_type.get(),
            self.current_photo_limits,
        )
        if self.intensity_factor is not None:
            for artist in self.intensity_factor:
                artist.remove()
            self.ax_photo.get_legend().remove()
            self.intensity_factor = None
        self.trace_intensity_factor()

        _apply_ax_theme(self.fig_photo, self.ax_photo, self._current_graph_theme()) # nouveau thème avant de tracer

        self.fig_photo.tight_layout()
        self.canvas_photo.draw()

    def trace_color(self):
        """
        Lit les données du fichier sélectionné et trace le graphique de colorimétrie.
        Affiche un avertissement si aucun fichier n'est sélectionné.
        """
        if not self._file_loaded():
            return

        self.data = orga.read_file(self.file_chosen)
        colo_file.trace_graph(self.data, self.ax_color)
        colo_file.trace_limit(self.ax_color)

        _apply_ax_theme(self.fig_photo, self.ax_photo, self._current_graph_theme()) # nouveau thème avant de tracer

        self.fig_photo.tight_layout()
        self.canvas_color.draw()

    def trace_intensity_factor(self):
        """
        Affiche ou masque la ligne du facteur d'intensité sur le graphique de photométrie
        en fonction de l'état de la variable de contrôle.
        """
        if self.current_photo_line:
            if self.var_intensity_factor.get():
                if self.var_secteur.get() == "Vide":
                    self.checkbox_intensity_factor.deselect()
                    tk.messagebox.showwarning(
                        "Avertissement: No sector",
                        "Veuillez d'abord choisir un secteur pour caculer le facteur d'intensité.",
                    )
                else:
                    if self.intensity_factor is None:
                        self.intensity_factor = photo_file.trace_factor(
                            self.ax_photo, self.data, self.var_secteur.get()
                        )
                        if self.intensity_factor is None:
                            self.checkbox_intensity_factor.deselect()
                            tk.messagebox.showwarning(
                                "Avertissement: Facteur d'intensité",
                                "Aucune valeur de courbe dans le secteur\nAucun facteur tracé",
                            )
                        else:
                            self.ax_photo.legend(loc="lower center")
            else:
                if self.intensity_factor is not None:
                    for artist in self.intensity_factor:
                        artist.remove()
                    self.ax_photo.get_legend().remove()
                    self.intensity_factor = None

            self.ax_photo.relim()
            self.ax_photo.autoscale_view()
            self.canvas_photo.draw()

        else:
            self.checkbox_intensity_factor.deselect()
            tk.messagebox.showwarning(
                "Avertissement: No graph",
                "Veuillez d'abord tracer un graphe.",
            )

    def file(self, _=None):
        """
        Ouvre une boîte de dialogue pour sélectionner
        un fichier et met à jour les labels d'information.

        Args:
            event: L'événement tkinter capturé.
        """
        path = orga.choisir_fichier()
        if not path:
            self.file_chosen = None
            self.label_fichier_photo.configure(text="Aucun fichier sélectionné")
            self.label_fichier_color.configure(text="Aucun fichier sélectionné")
            return

        self.file_chosen = path
        name = f"Fichier sélectionné : {'/'.join(self.file_chosen.split('/')[-3:])}"
        self.label_fichier_photo.configure(text=name)
        self.label_fichier_color.configure(text=name)
        self.ax_photo.set_autoscale_on(True)

    def enter_handel(self, _):
        """
        Gère l'événement de pression sur la touche Entrée pour lancer le traçage
        du graphique correspondant à l'onglet actif.

        Args:
            event: L'événement tkinter capturé.
        """
        current_tab = self.tabview.get()
        if current_tab == "Photométrie":
            self.trace_photo()
        elif current_tab == "Colorimétrie":
            self.trace_color()

    def switch_tab(self, _):
        """
        Gère l'événement de pression sur la touche Tab pour changer d'onglet de visualisation.

        Args:
            event: L'événement tkinter capturé.
        """
        if self.tabview.get() == "Photométrie":
            self.tabview.set("Colorimétrie")
        elif self.tabview.get() == "Colorimétrie":
            self.tabview.set("Photométrie")

    def decal_handle(self, key):
        """
        Gère l'événement de pression sur les touches de direction
        pour augmenter ou diminer le décalage du graphe.

        Args:
            key: L'événement tkinter capturé.
        """
        try:
            # val_decalage = float(self.var_decalage.get())
            val_decalage = eval(self.var_decalage.get())
        except NameError:
            tk.messagebox.showwarning(
                "Avertissement: Wrong value", "Le décalade doit être une valeur chiffrée"
            )
            val_decalage = 0
        except SyntaxError:
            tk.messagebox.showwarning(
                "Avertissement WRONG VALUE",
                """Le décalage DOIT être une valeur chiffrée. Vérifiez si un caractère ne s'y est pas glissé""",
            )
            val_decalage = 0

        if key.keysym == "Left":
            val_decalage -= 0.2
        elif key.keysym == "Right":
            val_decalage += 0.2
        elif key.keysym == "Up":
            val_decalage += 1
        elif key.keysym == "Down":
            val_decalage -= 1

        self.var_decalage.set(f"{val_decalage:0.1f}")

    def resize_handle(self, _):
        """
        Gère l'évenement de l'appuis de la touche R pour mettre à taille le graphe

        """
        self.ax_photo.set_autoscale_on(True)
        self.ax_photo.relim()
        self.ax_photo.autoscale_view()
        self.fig_photo.tight_layout()
        self.canvas_photo.draw()

        self.ax_color.set_autoscale_on(True)
        self.ax_color.relim()
        self.ax_color.autoscale_view()
        self.fig_color.tight_layout()
        self.canvas_color.draw()

    def changer_theme(self, new_theme):
        """
        Gère le changement de theme de l'application

        Args:
            new_theme: Le themes choisis.
        """
        ctk.set_appearance_mode(new_theme)
        self.after(50, self._refresh_graph_theme) # Petit délais d'affichage

    def _current_graph_theme(self):
        """Retourne 'dark' ou 'light' selon le thème CTk actif."""
        mode = ctk.get_appearance_mode().lower()
        if mode == "system":
            import darkdetect
            try:
                return "dark" if darkdetect.isDark() else "light"
            except Exception:
                return "light"
        return "dark" if mode == "dark" else "light"

    def _refresh_graph_theme(self):
        """Applique le thème courant aux deux figures matplotlib et redessine."""
        key = self._current_graph_theme()
        _apply_ax_theme(self.fig_photo, self.ax_photo, key)
        _apply_ax_theme(self.fig_color, self.ax_color, key)
        self.canvas_photo.draw()
        self.canvas_color.draw()

    def _toggle_live_update(self):
        """Active ou désactive la mise à jour automatique toutes les secondes."""
        if self._live_active:
            # ── Arrêt ──
            self._live_active = False
            if self._live_job:
                self.after_cancel(self._live_job)
                self._live_job = None
            self.button_live.configure(text="▶ Live")
        else:
            # ── Démarrage ──
            if not self._file_loaded():
                return
            self._live_active = True
            self.button_live.configure(text="⏹ Stop")
            self._live_tick()

    def _live_tick(self):
        """Appelé toutes les secondes tant que le mode live est actif."""
        if self._live_active:
            self.trace_photo()
            self._live_job = self.after(1000, self._live_tick)

    def a_propos(self):
        """
        Affiche un message d'à propos avec quelques informations

        """
        tk.messagebox.showinfo(
            "À propos",
            "Analyse Photométrique \n\nMantague - Breizelec.\n\nVersion v2.3",
        )


app = Application()
app.mainloop()
