"""
Archive : Ancienne version du script principal de l'application.
Regroupe la logique de sélection de fichier, de lecture et la structure
principale de l'interface utilisateur avant refactorisation.
"""
import pandas
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import photometry
import colorimetry

class Application(ctk.CTk):
    """Application principale avec système d'onglets"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.title("Analyse donnée feux de navigation")
        self.geometry("1100x800")
        self.minsize(900, 650)
        
        # Variables globales pour les fichiers
        self.fichier_selectionne = None
        self.dernier_dossier = "."
        
        # Créer le système d'onglets
        self.tabview = ctk.CTkTabview(self, width=1050, height=750)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        self.tabview.add("Photométrie")
        self.tabview.add("Colorimétrie")
        
        # Créer les instances des onglets
        self.photometry = photometry(self.tabview.tab("Photométrie"), self)
        self.colorimetry = colorimetry(self.tabview.tab("Colorimétrie"), self)
        
        # Key bindings globaux
        self.bind("<Return>", self.on_enter_pressed)
        self.bind("<KP_Enter>", self.on_enter_pressed)
    
    def on_enter_pressed(self, event):
        """Gère la touche Entrée pour tracer le graphique de l'onglet actif"""
        current_tab = self.tabview.get()
        if current_tab == "Photométrie":
            self.photometry.trace_graph()
        elif current_tab == "Colorimétrie":
            self.colorimetry.trace_graph()
    
    def choisir_fichier(self, tab_instance):
        """
        Choisir un fichier de données
        
        Args:
            tab_instance: Instance de l'onglet qui appelle cette fonction (PhotometryTab ou ColorimetryTab)
        """
        self.fichier_selectionne = filedialog.askopenfilename(
            title="Choisir un fichier de données",
            initialdir=self.dernier_dossier,
            filetypes=[
                ("Fichiers texte", "*.txt"),
                ("Fichiers de calcul", "*.csv"),
                ("Tous les fichiers", "*.*"),
            ],
        )
        
        if self.fichier_selectionne:
            self.dernier_dossier = "/".join(self.fichier_selectionne.split("/")[:-1])
            nom_fichier = self.fichier_selectionne.split("/")[-1]
            tab_instance.label_fichier.configure(
                text=f"Fichier sélectionné : {nom_fichier}"
            )
        else:
            tab_instance.label_fichier.configure(text="Aucun fichier sélectionné")
    
    def read_file(self):
        """
        Lit le fichier sélectionné et retourne un DataFrame pandas
        
        Returns:
            pandas.DataFrame: Les données du fichier, ou None si pas de fichier
        """
        if not self.fichier_selectionne:
            tk.messagebox.showwarning(
                "Avertissement: no file", "Veuillez d'abord choisir un fichier à ouvrir."
            )
            return None
        
        try:
            # Trouver les lignes à sauter
            lignes_a_sauter = set()
            with open(self.fichier_selectionne, "r") as f:
                lignes = f.readlines()
                for i, ligne in enumerate(lignes):
                    if "Angle" in ligne:
                        lignes_a_sauter.update(range(0, i), range(i + 1, i + 3))
                        break
            
            # Lire le fichier CSV
            data_file = pandas.read_csv(
                self.fichier_selectionne,
                sep=";",
                skiprows=lambda x: x in lignes_a_sauter,
                skipfooter=2,
                engine="python",
                usecols=["Angle °", "cd", "X", "Y", "lux"],
            )
            return data_file
        
        except Exception as e:
            tk.messagebox.showerror(
                "Erreur",
                f"Erreur lors de la lecture du fichier :\n{str(e)}"
            )
            return None


def main():
    """Point d'entrée de l'application"""
    app = Application()
    app.mainloop()


main()