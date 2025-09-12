# Arrera HTML Generator ✨

**Un convertisseur de documents universel avec une interface graphique moderne et un aperçu en direct.**

Transformez vos fichiers **.docx, .md, .odt et même .html** en pages web propres et stylisées. Visualisez vos modifications en temps réel grâce à l'aperçu intégré et exportez un fichier HTML parfait en un seul clic.



---

## 🚀 Fonctionnalités Clés

* **Multi-Format** : Convertissez depuis les formats les plus populaires :
    * Microsoft Word (`.docx`)
    * Markdown (`.md`)
    * OpenDocument Text (`.odt`)
    * Permet même de restyler un fichier `HTML` existant.
* **Aperçu en Direct** : Plus besoin de deviner ! Chaque changement de fichier ou de thème est immédiatement visible dans le panneau d'aperçu.
* **Thèmes CSS Personnalisables** : Appliquez instantanément un style à vos documents grâce aux thèmes CSS fournis. Ajoutez facilement les vôtres !
* **Interface Moderne** : Une interface utilisateur élégante avec un thème clair et sombre.
* **Autonome** : Le CSS est directement intégré dans le fichier HTML final, le rendant 100% portable.

---

## ✅ Prérequis

1.  **Python 3.8+**
2.  **Pandoc** : Pour la conversion des fichiers `.odt`, Pandoc doit être installé sur votre système.
    * [➡️ **Téléchargez et installez Pandoc ici**](https://pandoc.org/installing.html)

---

## 🛠️ Installation

Ce projet utilise un environnement virtuel pour une gestion propre des dépendances.

1.  **Clonez ou téléchargez ce projet.**

2.  **Ouvrez un terminal** dans le dossier du projet.

3.  **Créez l'environnement virtuel :**
    ```bash
    python -m venv venv
    ```

4.  **Activez l'environnement :**
    * Sur Windows (PowerShell) : `.\venv\Scripts\Activate.ps1`
    * Sur macOS/Linux : `source venv/bin/activate`

5.  **Installez les bibliothèques nécessaires :**
    ```bash
    pip install customtkinter mammoth pypandoc markdown beautifulsoup4 tkinterweb
    ```

---

## 🎨 Utilisation

Une fois l'installation terminée, lancez simplement l'application.

1.  **Assurez-vous que votre environnement est activé** (vous devez voir `(venv)` au début de votre terminal).

2.  **Exécutez le script :**
    ```bash
    python gui.py
    ```
3.  **Utilisez l'interface :**
    * **Cliquez sur "Parcourir..."** pour sélectionner votre fichier d'entrée.
    * **L'aperçu se met à jour** automatiquement.
    * **Changez le thème CSS** dans le menu déroulant pour voir le style changer en direct.
    * **Cliquez sur "Enregistrer sous..."** pour choisir où sauvegarder votre fichier.
    * Enfin, cliquez sur **"Convertir et Sauvegarder"**.

---

## ✨ Personnalisation

Pour ajouter vos propres thèmes, c'est très simple :
1.  Créez un nouveau fichier `.css` (ex: `mon_style.css`).
2.  Placez-le dans le dossier `styles/`.

3.  Relancez l'application : votre thème apparaîtra automatiquement dans le menu déroulant !
