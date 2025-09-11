import mammoth
import sys
import os # On importe le module 'os' pour gérer les chemins de fichiers

def convert_docx_to_html(docx_path, html_path, style_name=None):
    """
    Convertit un fichier .docx en un fichier .html complet,
    en y ajoutant optionnellement un lien vers une feuille de style CSS.
    
    Args:
        docx_path (str): Le chemin vers le fichier .docx d'entrée.
        html_path (str): Le chemin où sauvegarder le fichier .html de sortie.
        style_name (str, optional): Le nom du style CSS à appliquer (ex: 'dark').
    """
    try:
        # Étape 1: Conversion du .docx en contenu HTML (body seulement)
        with open(docx_path, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            body_content = result.value
            if result.messages:
                print("Messages de conversion :", result.messages, file=sys.stderr)

        # Étape 2: Création du lien CSS si un style est fourni
        css_link_tag = ''
        if style_name:
            css_file_path = f"styles/{style_name}.css"
            # On vérifie si le fichier CSS existe avant de créer le lien
            if os.path.exists(css_file_path):
                css_link_tag = f'<link rel="stylesheet" href="{css_file_path}">'
                print(f"🎨 Style '{style_name}' appliqué.")
            else:
                print(f"⚠️ Attention : Le fichier de style '{css_file_path}' n'existe pas. Aucun style ne sera appliqué.", file=sys.stderr)

        # Étape 3: Assemblage du document HTML final
        html_document = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(docx_path)}</title>
    {css_link_tag}
</head>
<body>
    {body_content}
</body>
</html>
"""
        # Étape 4: Écriture du fichier HTML final
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_document.strip())
            
        print(f"✅ Conversion réussie ! Fichier sauvegardé sous : {html_path}")

    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{docx_path}' n'a pas été trouvé.", file=sys.stderr)
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue : {e}", file=sys.stderr)

if __name__ == "__main__":
    # La commande attend maintenant 2 ou 3 arguments
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python convertisseur.py <entree.docx> <sortie.html> [nom_du_style]")
        print("Exemple avec style: python convertisseur.py doc.docx page.html dark")
        print("Exemple sans style: python convertisseur.py doc.docx page.html")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Le nom du style est optionnel
    style = sys.argv[3] if len(sys.argv) == 4 else None
    
    convert_docx_to_html(input_file, output_file, style)