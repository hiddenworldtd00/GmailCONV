# 📧 GmailCONV - Sauvegarde Avancée vers Gmail

**Créé par hacker_tchadien** 🇹🇩

> 🛡️ **Outil de sauvegarde sécurisé** - Envoyez vos fichiers importants sur Gmail avec organisation automatique, chiffrement et compression.

---

## 🎯 Objectif

GmailCONV permet de sauvegarder automatiquement vos fichiers sur Gmail en les organisant par type, avec:
- 📁 Organisation par labels Gmail
- 🔐 Chiffrement AES-256 optionnel
- 📦 Compression ZIP pour les gros fichiers
- 📊 Rapport détaillé de sauvegarde
- 🎨 Interface avec logo Gmail animé

---

## 🚀 Installation Rapide

```bash
# 1. Cloner ou télécharger le dossier GmailCONV
cd GmailCONV

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les credentials Google
python setup.py

# 4. Lancer la sauvegarde
python gmail_backup.py --folder ~/Documents --email votre.email@gmail.com
```

---

## 🔧 Configuration Google Cloud (Obligatoire)

### Étape 1: Créer un projet
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet nommé "GmailCONV"
3. Activez la **Gmail API**

### Étape 2: Créer les credentials OAuth2
1. APIs & Services → Credentials
2. Create Credentials → OAuth client ID
3. Configurez l'écran de consentement (Type: External)
4. Créez un client ID de type **Desktop app**
5. Téléchargez le fichier `credentials.json`

### Étape 3: Configuration locale
```bash
python setup.py
# Suivez les instructions et indiquez le chemin de credentials.json
```

---

## 📖 Utilisation

### Sauvegarde basique
```bash
python gmail_backup.py --folder ~/Documents --email mon.email@gmail.com
```

### Sauvegarde avec chiffrement
```bash
python gmail_backup.py --folder ~/Documents --email mon.email@gmail.com --encrypt --password "MonMotDePasseSecurise123!"
```

### Sauvegarde avec compression
```bash
python gmail_backup.py --folder ~/Documents --email mon.email@gmail.com --compress
```

### Sauvegarde récursive (avec sous-dossiers)
```bash
python gmail_backup.py --folder ~/Documents --email mon.email@gmail.com --recursive
```

### Exclure certains types
```bash
python gmail_backup.py --folder ~/Documents --email mon.email@gmail.com --exclude "*.tmp,*.log"
```

### Sauvegarde silencieuse (sans logo animé)
```bash
python gmail_backup.py --folder ~/Documents --email mon.email@gmail.com --no-logo
```

### Sauvegarde avec rapport HTML
```bash
python gmail_backup.py --folder ~/Documents --email mon.email@gmail.com --html
```

---

## 🎨 Logo Gmail Animé

Le logo Gmail animé s'affiche automatiquement au démarrage:

```
    ╔═══════════════════════════════════════╗
    ║         📧 GmailCONV 📧               ║
    ║    Sauvegarde Intelligente Gmail      ║
    ║                                       ║
    ║      ✉️  Gmail Logo Animé  ✉️         ║
    ║                                       ║
    ║    Créé par hacker_tchadien 🇹🇩       ║
    ╚═══════════════════════════════════════╝
```

Pour désactiver: utilisez `--no-logo`

---

## 📁 Organisation sur Gmail

Les fichiers sont organisés avec des labels:

```
GmailCONV/
├── Backup/          # Tous les fichiers sauvegardés
├── Documents/       # PDF, DOC, TXT...
├── Images/          # JPG, PNG, GIF...
├── Videos/          # MP4, AVI, MKV...
├── Audio/           # MP3, WAV, FLAC...
├── Archives/        # ZIP, RAR, 7Z...
├── Code/            # PY, JS, HTML...
├── Data/            # JSON, CSV, XML...
├── Large-Files/     # Fichiers > 24 Mo (découpés)
└── Encrypted/       # Fichiers chiffrés
```

---

## 🔐 Sécurité

- **OAuth2**: Authentification sécurisée sans stockage de mot de passe
- **Chiffrement AES-256**: Optionnel, mot de passe demandé interactivement
- **Token local**: Stocké localement dans `token.json`
- **Pas de données tierces**: Vos fichiers restent sur vos serveurs Gmail

---

## ⚠️ Limites de Gmail

| Limite | Valeur |
|--------|--------|
| Taille max pièce jointe | 25 Mo |
| Taille max email | 25 Mo |
| Stockage total | 15 Go (gratuit) |
| Emails par jour | 500 (compte gratuit) |

**Solution pour les gros fichiers:**
- Compression ZIP automatique
- Découpage en parties de 24 Mo
- Organisation par labels

---

## 🛠️ Architecture

```
GmailCONV/
├── gmail_backup.py      # Script principal (700+ lignes)
├── gmail_logo.py        # Logo animé ASCII
├── config.py            # Configuration
├── setup.py             # Script de configuration
├── requirements.txt     # Dépendances
└── README.md           # Documentation
```

---

## 📊 Rapport de Sauvegarde

Après chaque sauvegarde, un rapport est généré:

```
📊 RAPPORT DE SAUVEGARDE
═══════════════════════════════════════
📁 Dossier source: /home/user/Documents
📧 Email cible: user@gmail.com
📅 Date: 2024-01-15 14:30:00

📈 STATISTIQUES
  Total fichiers: 150
  Envoyés: 148
  Échoués: 2
  Taille totale: 1.2 Go

📁 PAR CATÉGORIE
  Documents: 45 fichiers (350 Mo)
  Images: 80 fichiers (600 Mo)
  Code: 23 fichiers (50 Mo)

⏱️ DURÉE: 5m 30s
✅ SAUVEGARDE TERMINÉE
```

---

## 🌍 Pour la Communauté Tchadienne

Cet outil est créé pour:
- Apprendre l'API Google (Gmail)
- Comprendre OAuth2 et l'authentification
- Maîtriser la manipulation de fichiers en Python
- Développer des outils de sauvegarde robustes
- Partager la connaissance technique

---

## 📝 Exemple Complet

```python
from gmail_backup import GmailBackup

# Initialiser
backup = GmailBackup("mon.email@gmail.com")

# Authentifier
backup.authenticate()

# Sauvegarder un dossier
result = backup.backup_folder(
    folder_path="/home/user/Documents",
    recursive=True,
    encrypt=True,
    password="MonMotDePasse123!",
    compress=True
)

# Afficher le rapport
backup.print_report(result)
```

---

## 🔗 Ressources

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google OAuth2 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Python Rich Library](https://rich.readthedocs.io/)

---

**© 2024 hacker_tchadien - Tous droits réservés**

*"La connaissance est une arme, utilisez-la à bon escient"*
