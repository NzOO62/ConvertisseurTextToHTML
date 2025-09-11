# ADOCX to HTML 📄✨

**Transformez vos documents Word (`.docx`) en pages HTML propres et stylisées, en une seule ligne de commande.**

Vous avez un document Word et vous rêvez de le publier sur le web sans vous battre avec du code HTML horrible généré par Word ? Cet outil est fait pour vous ! Il convertit vos fichiers `.docx` en un HTML sémantique et propre, et vous permet même d'appliquer de magnifiques thèmes CSS (Clair, Sombre, Professionnel, et plus encore) à la volée.

---

## 🚀 Fonctionnalités

* **Conversion Sémantique** : Fini le code pollué ! Les titres deviennent des `<h1>`, `<h2>`, les listes des `<ul>`, les tableaux des `<table>`, etc.
* **Thèmes CSS** : Appliquez un style à votre page HTML instantanément. Passez d'un look `light` à `dark` en un clin d'œil.
* **Extrêmement Simple** : Aucune interface compliquée. Tout se passe dans votre terminal.
* **Gestion des Images** : Les images de votre document sont automatiquement intégrées dans la page HTML.
* **Extensible** : Créez facilement vos propres thèmes CSS pour correspondre à votre identité visuelle.

---

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé :

* [Python 3.6+](https://www.python.org/downloads/)
* `pip` (généralement inclus avec Python)

---

## 🛠️ Installation

1.  **Clonez ou téléchargez ce projet :**

    ```bash
    git clone [https://github.com/votre-nom-utilisateur/votre-projet.git](https://github.com/votre-nom-utilisateur/votre-projet.git)
    cd votre-projet
    ```

2.  **Installez la dépendance nécessaire :**

    Le projet utilise la bibliothèque `mammoth`. Installez-la avec `pip`.

    ```bash
    pip install mammoth
    ```

3.  **Vérifiez la structure des fichiers :**

    Assurez-vous que la structure de votre projet ressemble à ceci :

    ```
    .
    ├── convertisseur.py      # Le script principal
    ├── README.md             # Ce fichier
    └── styles/
        ├── light.css
        ├── dark.css
        └── professional.css
    ```

---

## 🎨 Comment l'utiliser

L'utilisation se fait via la ligne de commande. La syntaxe est simple :

```bash
python convertisseur.py <fichier_entree.docx> <fichier_sortie.html> [theme_optionnel]
Exemples :
1. Conversion simple (sans style)

Bash

python convertisseur.py mon_rapport.docx page_web.html
Le fichier page_web.html sera créé avec un style de navigateur par défaut.

2. Conversion avec le thème sombre

Bash

python convertisseur.py rapport_science.docx article_sombre.html dark
La page article_sombre.html sera générée avec le style dark.css.

3. Conversion avec le thème professionnel

Bash

python convertisseur.py CV.docx mon_cv_en_ligne.html professional
Votre CV est maintenant une page web propre avec une touche professionnelle !

✨ Créez vos propres thèmes
Vous voulez un thème à vos couleurs ? C'est très simple !

Créez un nouveau fichier CSS dans le dossier styles/, par exemple mon_theme.css.

Ajoutez-y vos règles de style.

Utilisez-le en appelant le script avec le nom de votre fichier (sans l'extension) :

Bash

python convertisseur.py mon_doc.docx ma_page_perso.html mon_theme
🤝 Contribuer
Les contributions sont les bienvenues ! Si vous avez des idées d'amélioration, des corrections de bugs ou de nouveaux thèmes à proposer, n'hésitez pas à ouvrir une issue ou une pull request.

