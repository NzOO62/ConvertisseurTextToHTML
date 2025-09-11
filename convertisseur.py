import mammoth
import sys

def convert_docx_to_html(docx_path, html_path):
    """
    Convertit un fichier .docx en un fichier .html propre.
    
    Args:
        docx_path (str): Le chemin vers le fichier .docx d'entrée.
        html_path (str): Le chemin où sauvegarder le fichier .html de sortie.
    """
    try:
        # Ouvre le fichier docx en mode lecture binaire ('rb')
        with open(docx_path, 'rb') as docx_file:
            # Effectue la conversion
            result = mammoth.convert_to_html(docx_file)
            
            # Récupère le contenu HTML généré
            html_content = result.value 
            
            # Affiche les messages éventuels (avertissements, erreurs)
            if result.messages:
                print("Messages de conversion :", result.messages, file=sys.stderr)

        # Écrit le contenu HTML dans le fichier de sortie en encodage UTF-8
        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
            
        print(f"✅ Conversion réussie ! Fichier sauvegardé sous : {html_path}")

    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier '{docx_path}' n'a pas été trouvé.", file=sys.stderr)
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue : {e}", file=sys.stderr)

if __name__ == "__main__":
    # Vérifie que les arguments (noms de fichiers) ont bien été fournis en ligne de commande
    if len(sys.argv) != 3:
        print("Usage: python convertisseur.py <fichier_entree.docx> <fichier_sortie.html>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_docx_to_html(input_file, output_file)