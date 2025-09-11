import customtkinter as ctk
from tkinter import filedialog
import os

# --- Début de la logique de conversion MODIFIÉE ---
import mammoth

def convert_docx_to_html(docx_path, html_path, style_name=None):
    """
    Logique de conversion qui EMBARQUE maintenant le CSS directement dans le HTML.
    """
    # Étape 1: Conversion du .docx en contenu HTML (body seulement)
    with open(docx_path, 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        body_content = result.value
    
    # Étape 2: Intégration du CSS si un style est fourni
    html_style_block = '' # Le bloc sera vide si aucun style n'est choisi
    if style_name and style_name != "Aucun thème":
        css_file_path = f"styles/{style_name}.css"
        if os.path.exists(css_file_path):
            with open(css_file_path, 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
                # On crée une balise <style> avec le contenu du CSS
                html_style_block = f"<style>\n{css_content}\n</style>"
    
    # Étape 3: Assemblage du document HTML final avec le style intégré
    html_document = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(docx_path)}</title>
    {html_style_block}
</head>
<body>
    {body_content}
</body>
</html>
"""
    # Étape 4: Écriture du fichier HTML final
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_document.strip())
# --- Fin de la logique de conversion ---


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuration de la fenêtre principale ---
        self.title("ADOCX to HTML ✨")
        self.geometry("700x420")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # --- Variables pour stocker l'état ---
        self.input_file_path = ctk.StringVar(value="Aucun fichier sélectionné")

        # --- Création des widgets ---
        self.create_widgets()
    
    def create_widgets(self):
        # Frame pour la sélection de fichier
        file_frame = ctk.CTkFrame(self)
        file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        file_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(file_frame, text="Fichier DOCX", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(file_frame, textvariable=self.input_file_path, text_color="gray").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(file_frame, text="Parcourir...", command=self.select_file).grid(row=1, column=1, padx=10, pady=10)

        # Frame pour les options de conversion
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(options_frame, text="Thème CSS", font=ctk.CTkFont(size=14, weight="bold")).pack(padx=10, pady=5, anchor="w")
        
        # Détection automatique des thèmes CSS
        themes = self.scan_themes()
        self.theme_menu = ctk.CTkOptionMenu(options_frame, values=themes)
        self.theme_menu.pack(padx=10, pady=10, fill="x")
        self.theme_menu.set(themes[0] if themes else "Aucun thème trouvé")

        # Bouton principal de conversion
        self.convert_button = ctk.CTkButton(self, text="Convertir en HTML", command=self.convert, height=40, font=ctk.CTkFont(size=16, weight="bold"))
        self.convert_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        # Label pour les messages de statut
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Switch pour le mode d'apparence (Dark/Light)
        self.appearance_switch = ctk.CTkSwitch(self, text="Mode Sombre", command=self.change_appearance_mode)
        self.appearance_switch.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.appearance_switch.select()

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier Word", filetypes=[("Documents Word", "*.docx")])
        if file_path:
            self.input_file_path.set(file_path)
            self.status_label.configure(text="")

    def scan_themes(self):
        styles_dir = "styles"
        if not os.path.isdir(styles_dir):
            return ["Aucun thème"]
        themes = [f.replace(".css", "") for f in os.listdir(styles_dir) if f.endswith(".css")]
        return ["Aucun thème"] + themes if themes else ["Aucun thème"]

    def convert(self):
        input_path = self.input_file_path.get()
        if not os.path.exists(input_path):
            self.status_label.configure(text="❌ Erreur : Veuillez sélectionner un fichier valide.", text_color="red")
            return

        output_path = os.path.splitext(input_path)[0] + ".html"
        selected_theme = self.theme_menu.get()

        try:
            convert_docx_to_html(input_path, output_path, selected_theme)
            self.status_label.configure(text=f"✅ Succès ! Fichier sauvegardé sous : {output_path}", text_color="green")
        except Exception as e:
            self.status_label.configure(text=f"❌ Erreur lors de la conversion : {e}", text_color="red")

    def change_appearance_mode(self):
        new_mode = "Dark" if self.appearance_switch.get() else "Light"
        ctk.set_appearance_mode(new_mode)

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = App()
    app.mainloop()