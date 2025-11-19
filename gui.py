import customtkinter as ctk
from tkinter import filedialog
import os
import mammoth
# NOUVEAUX IMPORTS
import pypandoc
import markdown
from bs4 import BeautifulSoup
import tkinterweb
import webbrowser
# --- MOTEURS DE CONVERSION ---

def convert_docx_to_html(docx_path, style_name=None):
    with open(docx_path, 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

def convert_md_to_html(md_path):
    with open(md_path, 'r', encoding='utf-8') as md_file:
        text = md_file.read()
        return markdown.markdown(text, extensions=['fenced_code', 'tables'])

def convert_odt_to_html(odt_path):
    # Pandoc gère la conversion complète
    return pypandoc.convert_file(odt_path, 'html')

def apply_theme_to_html(html_path, style_name=None):
    with open(html_path, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    
    # On retourne le corps (body) du HTML pour l'envelopper ensuite
    if soup.body:
        return str(soup.body)
    return "" # Retourne une chaîne vide si aucun body n'est trouvé

# --- FONCTION D'ASSEMBLAGE FINAL ---

def build_final_html(body_content, title, style_name=None):
    """Prend un corps HTML et l'enveloppe dans une structure complète avec un thème."""
    html_style_block = ''
    if style_name and style_name != "Aucun thème":
        css_file_path = f"styles/{style_name}.css"
        if os.path.exists(css_file_path):
            with open(css_file_path, 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
                html_style_block = f"<style>\n{css_content}\n</style>"
    
    html_document = f"""
<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>{html_style_block}</head><body>{body_content}</body></html>
"""
    return html_document.strip()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Arrera HTML Generator (Multi-Format)")
        self.geometry("1100x700")
        self.grid_columnconfigure(0, weight=1, minsize=350)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        self.input_file_path = ctk.StringVar(value="")
        self.output_file_path = ctk.StringVar(value="")
        self.current_html_content = ""
        self.create_widgets()
    
    def create_widgets(self):
        # --- Colonne de gauche : Panneau de contrôle ---
        control_frame = ctk.CTkFrame(self, width=350)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        control_frame.grid_rowconfigure(3, weight=1)

        input_frame = ctk.CTkFrame(control_frame)
        input_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(input_frame, text="1. Fichier d'Entrée (.docx, .md, .odt, .html)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        ctk.CTkButton(input_frame, text="Parcourir...", command=self.select_input_file).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.input_label = ctk.CTkLabel(input_frame, text="Aucun fichier sélectionné", text_color="gray", wraplength=280)
        self.input_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        output_frame = ctk.CTkFrame(control_frame)
        output_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        output_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(output_frame, text="2. Fichier HTML (Sortie)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        ctk.CTkButton(output_frame, text="Enregistrer sous...", command=self.select_output_file).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.output_label = ctk.CTkLabel(output_frame, text="Aucun emplacement défini", text_color="gray", wraplength=280)
        self.output_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        options_frame = ctk.CTkFrame(control_frame)
        options_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(options_frame, text="3. Thème CSS", font=ctk.CTkFont(size=14, weight="bold")).pack(padx=10, pady=5, anchor="w")
        themes = self.scan_themes()
        self.theme_menu = ctk.CTkOptionMenu(options_frame, values=themes, command=self.on_theme_change)
        self.theme_menu.pack(padx=10, pady=5, fill="x")
        self.theme_menu.set(themes[0] if themes else "Aucun thème")
        
        bottom_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        bottom_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)
        self.convert_button = ctk.CTkButton(bottom_frame, text="Convertir et Sauvegarder", command=self.convert, height=40, font=ctk.CTkFont(size=16, weight="bold"))
        self.convert_button.grid(row=0, column=0, sticky="ew")
        self.status_label = ctk.CTkLabel(bottom_frame, text="", height=1)
        self.status_label.grid(row=1, column=0, pady=(10, 0), sticky="ew")
        self.appearance_switch = ctk.CTkSwitch(bottom_frame, text="Mode Sombre", command=self.change_appearance_mode)
        self.appearance_switch.grid(row=2, column=0, pady=(10, 0), sticky="w")
        self.appearance_switch.select()

        # --- Colonne de droite : Aperçu en direct ---
        preview_frame = ctk.CTkFrame(self)
        preview_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.html_preview = tkinterweb.HtmlFrame(preview_frame)
        self.html_preview.pack(expand=True, fill="both")
        self.html_preview.load_html("<h1>Aperçu en direct</h1><p>Sélectionnez un fichier .docx, .md, .odt ou .html pour commencer.</p>")
        btn_frame = ctk.CTkFrame(preview_frame, height=40)
        btn_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="🌍 Voir dans le Navigateur (Rendu Réel)", 
            command=self.open_in_browser).pack(expand=True, fill="both")

    def update_preview(self):
        input_path = self.input_file_path.get()
        if not input_path or not os.path.exists(input_path):
            self.html_preview.load_html("<h1>Aucun fichier valide sélectionné</h1>")
            return
        
        try:
            selected_theme = self.theme_menu.get()
            file_title = os.path.basename(input_path)
            body_content = ""

            # MODIFIÉ : Le "cerveau" qui choisit le bon moteur de conversion
            if input_path.lower().endswith('.docx'):
                body_content = convert_docx_to_html(input_path)
            elif input_path.lower().endswith('.md'):
                body_content = convert_md_to_html(input_path)
            elif input_path.lower().endswith('.odt'):
                body_content = convert_odt_to_html(input_path)
            elif input_path.lower().endswith(('.html', '.htm')):
                body_content = apply_theme_to_html(input_path)
            else:
                body_content = "<h1>Format de fichier non supporté</h1>"

            # On assemble le HTML final avec le thème
            html_content = build_final_html(body_content, file_title, selected_theme)
            
            self.current_html_content = html_content
            self.html_preview.load_html(html_content)
            self.status_label.configure(text="")
        except Exception as e:
            error_message = f"<h1>Erreur de conversion</h1><p>Fichier: {os.path.basename(input_path)}</p><p>Erreur: {e}</p>"
            self.html_preview.load_html(error_message)
            self.status_label.configure(text=f"❌ Erreur lors de la génération de l'aperçu.", text_color=("red", "#E57373"))

    def select_input_file(self):
        # MODIFIÉ : Accepte plusieurs types de fichiers
        file_path = filedialog.askopenfilename(
            title="Sélectionnez un fichier",
            filetypes=[
                ("Documents Supportés", "*.docx *.md *.odt *.html *.htm"),
                ("Documents Word", "*.docx"),
                ("Fichiers Markdown", "*.md"),
                ("Documents OpenDocument", "*.odt"),
                ("Fichiers HTML", "*.html *.htm"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if file_path: self.set_input_file(file_path)

    # --- Les autres fonctions (set_input_file, on_theme_change, convert, etc.) restent les mêmes ---
    def set_input_file(self, file_path):
        self.input_file_path.set(file_path); self.input_label.configure(text=os.path.basename(file_path))
        suggested_output = os.path.splitext(file_path)[0] + "_converti.html"
        self.output_file_path.set(suggested_output); self.output_label.configure(text=os.path.basename(suggested_output))
        self.update_preview()
    def on_theme_change(self, choice): self.update_preview()
    def convert(self):
        output_path = self.output_file_path.get()
        if not output_path or "Aucun emplacement" in output_path: self.status_label.configure(text="❌ Erreur : Veuillez définir un emplacement de sortie.", text_color=("red", "#E57373")); return
        try:
            html_to_save = self.current_html_content
            if not html_to_save: self.status_label.configure(text="❌ Erreur : Aucun aperçu à sauvegarder.", text_color=("red", "#E57373")); return
            with open(output_path, "w", encoding="utf-8") as f: f.write(html_to_save)
            self.status_label.configure(text="✅ Succès ! Fichier sauvegardé.", text_color=("green", "#81C784"))
        except Exception as e: self.status_label.configure(text=f"❌ Erreur lors de la sauvegarde : {e}", text_color=("red", "#E57373"))
    def select_output_file(self):
        input_path = self.input_file_path.get(); initial_file = "sortie.html"
        if os.path.exists(input_path): initial_file = os.path.basename(os.path.splitext(input_path)[0] + "_converti.html")
        file_path = filedialog.asksaveasfilename(title="Enregistrer le fichier HTML sous...", defaultextension=".html", initialfile=initial_file, filetypes=[("Fichiers HTML", "*.html")])
        if file_path: self.output_file_path.set(file_path); self.output_label.configure(text=os.path.basename(file_path))
    def scan_themes(self):
        styles_dir = "styles";
        if not os.path.isdir(styles_dir): return ["Aucun thème"]
        themes = [f.replace(".css", "") for f in os.listdir(styles_dir) if f.endswith(".css")]
        return ["Aucun thème"] + themes if themes else ["Aucun thème"]
    def change_appearance_mode(self): ctk.set_appearance_mode("Dark" if self.appearance_switch.get() else "Light")

    def open_in_browser(self):
        if not self.current_html_content:
            return
        # On crée un fichier temporaire pour l'aperçu
        import tempfile
        temp_file = os.path.join(tempfile.gettempdir(), "preview_arrera.html")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(self.current_html_content)
        # On l'ouvre avec le navigateur par défaut
        webbrowser.open('file://' + temp_file)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()