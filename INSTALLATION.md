# 🔧 Guide d'Installation Pas à Pas

**Créé par hacker_tchadien**

---

## 📋 Prérequis Communs

### 1. Installer Python

**Windows:**
1. Va sur [python.org/downloads](https://www.python.org/downloads/)
2. Télécharge Python 3.10+ (bouton jaune)
3. Lance l'installateur
4. ✅ **Coche "Add Python to PATH"** (IMPORTANT!)
5. Clique "Install Now"
6. Vérifie: ouvre CMD et tape `python --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
python3 --version
```

**Mac:**
```bash
# Installe Homebrew d'abord
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Puis Python
brew install python
python3 --version
```

### 2. Installer Git (optionnel mais recommandé)

**Windows:** [git-scm.com/download/win](https://git-scm.com/download/win)

**Linux:**
```bash
sudo apt install git -y
```

**Mac:**
```bash
brew install git
```

---

## 🟢 Projet 1: ALLIM.py (Script Python)

### Installation

```bash
# 1. Ouvre un terminal
# Windows: Win+R → cmd
# Linux/Mac: Ctrl+Alt+T

# 2. Va dans le dossier
cd /chemin/vers/ALLIM.py

# 3. Vérifie Python
python --version
# ou sur Linux/Mac:
python3 --version

# 4. Lance le script
python ALLIM.py
# ou:
python3 ALLIM.py
```

### Résolution des problèmes

**"python" n'est pas reconnu:**
- Windows: Réinstalle Python en cochant "Add to PATH"
- Linux: Utilise `python3` au lieu de `python`

**Erreur de syntaxe:**
- Vérifie que tu as Python 3.10+
- Télécharge à nouveau le fichier

---

## 🌐 Projet 2: ALLIM Web (Site Complet)

### Étape 1: Backend

```bash
# 1. Va dans le dossier backend
cd allim-web/backend

# 2. Crée un environnement virtuel
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# 3. Installe les dépendances
pip install -r requirements.txt

# 4. Crée la base de données
python init_db.py

# 5. Lance le serveur
python app.py

# Le backend est sur http://localhost:5000
```

### Étape 2: Frontend

**Méthode 1 - Simple (recommandé pour débutant):**
```bash
# Ouvre directement le fichier dans le navigateur
# Double-clique sur allim-web/frontend/index.html
```

**Méthode 2 - Serveur local:**
```bash
cd allim-web/frontend

# Avec Python:
python -m http.server 8080

# Ou avec Node.js (si installé):
npx serve .

# Le site est sur http://localhost:8080
```

### Étape 3: Vérifier que tout fonctionne

1. Backend doit afficher: `Running on http://localhost:5000`
2. Frontend doit afficher la page avec le logo ALLIM
3. Teste l'inscription sur le site

---

## 📱 Projet 3: WHAT-YOU (Analyseur WhatsApp)

### Installation

```bash
# 1. Va dans le dossier
cd WHAT-YOU

# 2. Installe les dépendances
pip install -r requirements.txt

# 3. Teste avec l'exemple
python test_analyzer.py

# 4. Voir le guide d'export
python export_guide.py
```

### Exporter une conversation WhatsApp

**Android:**
1. Ouvre WhatsApp
2. Appuie longuement sur la conversation
3. Menu (3 points) → "Plus" → "Exporter la discussion"
4. Choisis "Sans médias" pour commencer
5. Envoie-toi le fichier par email

**iPhone:**
1. Paramètres → Discussions → Exporter la discussion
2. Choisis la conversation
3. Envoie par email

### Analyser l'export

```bash
# Décompresse le fichier reçu
# Tu auras un dossier "WhatsApp Chat avec [Nom]"

# Analyse
python whatsapp_analyzer.py --input "/chemin/vers/le/dossier"
```

---

## 📧 Projet 4: GmailCONV (Sauvegarde Gmail)

### Étape 1: Créer un projet Google Cloud

1. Va sur [console.cloud.google.com](https://console.cloud.google.com)
2. Connecte-toi avec ton compte Google
3. Clique sur le sélecteur de projet (en haut)
4. "New Project"
5. Nom: "GmailCONV"
6. Clique "Create"

### Étape 2: Activer l'API Gmail

1. Menu ≡ (haut gauche)
2. "APIs & Services" → "Library"
3. Cherche "Gmail API"
4. Clique dessus
5. Clique "Enable"

### Étape 3: Créer les credentials

1. Menu ≡ → "APIs & Services" → "Credentials"
2. Clique "Create Credentials"
3. Choisis "OAuth client ID"
4. Si demandé, configure l'écran de consentement:
   - User Type: "External"
   - App name: "GmailCONV"
   - User support email: ton email
   - Developer contact: ton email
   - Sauvegarde
5. Application type: "Desktop app"
6. Name: "GmailCONV Desktop"
7. Clique "Create"
8. Clique "Download JSON"

### Étape 4: Configurer GmailCONV

```bash
# 1. Va dans le dossier
cd GmailCONV

# 2. Installe les dépendances
pip install -r requirements.txt

# 3. Lance la configuration
python setup.py

# 4. Quand demandé, donne le chemin du fichier credentials.json téléchargé
# Exemple: C:\Users\TonNom\Downloads\credentials.json
```

### Étape 5: Utiliser GmailCONV

```bash
# Voir le logo animé
python gmail_logo.py

# Sauvegarder un dossier
python gmail_backup.py --folder ~/Documents --email ton.email@gmail.com

# Options avancées
python gmail_backup.py --help
```

### Première authentification

La première fois, GmailCONV va:
1. Ouvrir ton navigateur
2. Te demander de te connecter à Google
3. Demander l'autorisation d'accéder à Gmail
4. Générer un token de sécurité

Le token est sauvegardé dans `token.json` pour les prochaines fois.

---

## 🛠️ Outils Recommandés

### Éditeur de Code
- **VS Code** (Gratuit): [code.visualstudio.com](https://code.visualstudio.com)
- **PyCharm Community** (Gratuit): [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)

### Terminal
- **Windows**: Windows Terminal (Microsoft Store)
- **Linux**: Terminal natif
- **Mac**: iTerm2

### Navigateur
- **Chrome** ou **Firefox** (pour les projets web)

---

## 🆘 Dépannage

### "pip n'est pas reconnu"
```bash
# Windows
python -m pip install --upgrade pip

# Linux/Mac
python3 -m pip install --upgrade pip
```

### "Permission denied"
```bash
# Linux/Mac
sudo pip install -r requirements.txt

# Ou mieux, utilise un environnement virtuel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Erreur de port déjà utilisé
```bash
# Trouve le processus
# Windows:
netstat -ano | findstr :5000
# Linux/Mac:
lsof -i :5000

# Tue le processus ou change le port
python app.py --port 5001
```

### Problèmes de CORS (web)
Vérifie que le backend et frontend sont bien lancés.
Le backend doit être sur le port 5000.

---

## 📞 Besoin d'aide?

1. Relis le README de chaque projet
2. Vérifie les prérequis
3. Cherche l'erreur sur Google
4. Demande de l'aide à la communauté

**Créé par hacker_tchadien**
