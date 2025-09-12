import customtkinter as ctk
from tkinter import filedialog
import os
import mammoth
import tkinterweb

def convert_docx_to_html(docx_path, style_name=None):
    with open(docx_path, 'rb') as docx_file:
        result = mammoth.convert_to_html(docx_file)
        body_content = result.value
    
    html_style_block = ''
    if style_name and style_name != "Aucun thème":
        css_file_path = f"styles/{style_name}.css"
        if os.path.exists(css_file_path):
            with open(css_file_path, 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
                html_style_block = f"<style>\n{css_content}\n</style>"
    
    html_document = f"""
<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{os.path.basename(docx_path)}</title>{html_style_block}</head><body>{body_content}</body></html>
"""
    return html_document.strip()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ADOCX to HTML ✨ (avec Aperçu en direct)")
        self.geometry("1100x700")

        self.grid_columnconfigure(0, weight=1, minsize=350)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        self.input_file_path = ctk.StringVar(value="")
        self.output_file_path = ctk.StringVar(value="")
        
        # AJOUT : Une variable pour garder en mémoire le dernier HTML généré
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
        ctk.CTkLabel(input_frame, text="1. Fichier DOCX (Entrée)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
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
        self.html_preview.load_html("<h1>Aperçu en direct</h1><p>Veuillez sélectionner un fichier .docx pour commencer.</p>")

    def update_preview(self):
        if not self.input_file_path.get() or not os.path.exists(self.input_file_path.get()):
            self.html_preview.load_html("<h1>Aucun fichier valide sélectionné</h1>")
            return
        
        try:
            selected_theme = self.theme_menu.get()
            html_content = convert_docx_to_html(self.input_file_path.get(), selected_theme)
            
            # MODIFIÉ : On stocke le HTML généré dans notre variable
            self.current_html_content = html_content
            
            self.html_preview.load_html(html_content)
            self.status_label.configure(text="")
        except Exception as e:
            self.html_preview.load_html(f"<h1>Erreur de conversion</h1><p>{e}</p>")
            self.status_label.configure(text=f"❌ Erreur lors de la génération de l'aperçu.", text_color=("red", "#E57373"))

    def set_input_file(self, file_path):
        self.input_file_path.set(file_path)
        self.input_label.configure(text=os.path.basename(file_path))
        suggested_output = os.path.splitext(file_path)[0] + ".html"
        self.output_file_path.set(suggested_output)
        self.output_label.configure(text=os.path.basename(suggested_output))
        self.update_preview()

    def select_input_file(self):
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier Word", filetypes=[("Documents Word", "*.docx")])
        if file_path: self.set_input_file(file_path)

    def on_theme_change(self, choice):
        self.update_preview()

    def convert(self):
        output_path = self.output_file_path.get()
        if not output_path or "Aucun emplacement" in output_path:
            self.status_label.configure(text="❌ Erreur : Veuillez définir un emplacement de sortie.", text_color=("red", "#E5T373"))
            return
            
        try:
            # MODIFIÉ : On utilise notre variable stockée au lieu d'appeler une fonction inexistante
            html_to_save = self.current_html_content
            if not html_to_save:
                self.status_label.configure(text="❌ Erreur : Aucun aperçu à sauvegarder. Sélectionnez un fichier d'abord.", text_color=("red", "#E57373"))
                return

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_to_save)
            self.status_label.configure(text="✅ Succès ! Fichier sauvegardé.", text_color=("green", "#81C784"))
        except Exception as e:
            self.status_label.configure(text=f"❌ Erreur lors de la sauvegarde : {e}", text_color=("red", "#E57373"))
    
    def select_output_file(self):
        input_path = self.input_file_path.get(); initial_file = "sortie.html"
        if os.path.exists(input_path): initial_file = os.path.basename(os.path.splitext(input_path)[0] + ".html")
        file_path = filedialog.asksaveasfilename(title="Enregistrer le fichier HTML sous...", defaultextension=".html", initialfile=initial_file, filetypes=[("Fichiers HTML", "*.html")])
        if file_path: self.output_file_path.set(file_path); self.output_label.configure(text=os.path.basename(file_path))

    def scan_themes(self):
        styles_dir = "styles";
        if not os.path.isdir(styles_dir): return ["Aucun thème"]
        themes = [f.replace(".css", "") for f in os.listdir(styles_dir) if f.endswith(".css")]
        return ["Aucun thème"] + themes if themes else ["Aucun thème"]

    def change_appearance_mode(self): ctk.set_appearance_mode("Dark" if self.appearance_switch.get() else "Light")

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()