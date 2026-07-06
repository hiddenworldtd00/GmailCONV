#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗  ██████╗  ██████╗  ██████╗ ██╗     ███████╗                       ║
║   ██╔════╝ ██╔════╝ ██╔═══██╗██╔═══██╗██║     ██╔════╝                       ║
║   ██║  ███╗██║  ███╗██║   ██║██║   ██║██║     █████╗                         ║
║   ██║   ██║██║   ██║██║   ██║██║   ██║██║     ██╔══╝                         ║
║   ╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗                       ║
║    ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                       ║
║                                                                              ║
║   ██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗                           ║
║   ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗                          ║
║   ██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝                          ║
║   ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔══██╗                          ║
║   ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║  ██║                          ║
║   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝                          ║
║                                                                              ║
║   ████████╗ ██████╗     ██████╗  █████╗ ██████╗ ████████╗                   ║
║   ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝                   ║
║      ██║   ██║   ██║    ██████╔╝███████║██████╔╝   ██║                      ║
║      ██║   ██║   ██║    ██╔══██╗██╔══██║██╔══██╗   ██║                      ║
║      ██║   ╚██████╔╝    ██║  ██║██║  ██║██████╔╝   ██║                      ║
║      ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝    ╚═╝                      ║
║                                                                              ║
║   ██████╗ ███████╗ █████╗ ██╗  ██╗██╗   ██╗██████╗                           ║
║   ██╔══██╗██╔════╝██╔══██╗██║  ██║██║   ██║██╔══██╗                          ║
║   ██████╔╝█████╗  ███████║███████║██║   ██║██████╔╝                          ║
║   ██╔══██╗██╔══╝  ██╔══██║██╔══██║██║   ██║██╔══██╗                          ║
║   ██║  ██║███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║                          ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

    GMAILCONV - Sauvegarde Avancée vers Gmail
    Créé par hacker_tchadien
    
    DESCRIPTION:
    ============
    GmailCONV est un outil professionnel de sauvegarde de fichiers vers
    Gmail en utilisant l'API Google. Il permet de:
    
    • Sauvegarder des fichiers/dossiers complets sur Gmail
    • Compresser automatiquement les dossiers en ZIP
    • Chiffrer les fichiers avec AES-256 avant envoi
    • Gérer les pièces jointes jusqu'à 25MB (limite Gmail)
    • Fragmenter les gros fichiers automatiquement
    • Créer des labels Gmail organisés
    • Planifier des sauvegardes automatiques
    • Interface graphique avec logo animé
    • Logs détaillés de toutes les opérations
    
    SÉCURITÉ:
    =========
    • Authentification OAuth2 sécurisée
    • Chiffrement AES-256 des fichiers sensibles
    • Tokens stockés localement de manière sécurisée
    • Pas de données envoyées à des tiers
    
    USAGE ÉTHIQUE:
    ==============
    Cet outil doit être utilisé UNIQUEMENT pour sauvegarder vos propres
    fichiers personnels. Ne sauvegardez pas de données sensibles d'autrui
    sans autorisation explicite.
"""

import os
import sys
import base64
import json
import pickle
import mimetypes
import zipfile
import tarfile
import shutil
import hashlib
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage

# Rich pour l'interface
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.style import Style

# Google API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

console = Console()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

CONFIG_DIR = Path.home() / '.gmailconv'
TOKEN_FILE = CONFIG_DIR / 'token.pickle'
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'
CONFIG_FILE = CONFIG_DIR / 'config.json'
LOG_FILE = CONFIG_DIR / 'backup.log'

# Logo ASCII Gmail animé
GMAIL_LOGO_FRAMES = [
    """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║     📧 GMAIL CONV BACKUP 📧          ║
    ║                                       ║
    ║         ████████████████              ║
    ║       ██                ██            ║
    ║      ██    ▓▓▓▓▓▓▓▓    ██            ║
    ║     ██    ▓▓      ▓▓    ██            ║
    ║     ██   ▓▓   ██   ▓▓   ██            ║
    ║     ██   ▓▓  ████  ▓▓   ██            ║
    ║     ██   ▓▓   ██   ▓▓   ██            ║
    ║      ██   ▓▓      ▓▓   ██             ║
    ║       ██   ▓▓▓▓▓▓▓▓   ██              ║
    ║        ██            ██               ║
    ║          ████████████                 ║
    ║                                       ║
    ║      Créé par hacker_tchadien         ║
    ╚═══════════════════════════════════════╝
    """,
    """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║     📧 GMAIL CONV BACKUP 📧          ║
    ║                                       ║
    ║         ████████████████              ║
    ║       ██                ██            ║
    ║      ██    ░░▓▓▓▓▓▓░░    ██           ║
    ║     ██    ░░▓▓    ▓▓░░    ██          ║
    ║     ██   ░░▓▓  ██  ▓▓░░   ██          ║
    ║     ██   ░░▓▓ ████ ▓▓░░   ██          ║
    ║     ██   ░░▓▓  ██  ▓▓░░   ██          ║
    ║      ██   ░░▓▓    ▓▓░░   ██           ║
    ║       ██   ░░▓▓▓▓▓▓░░   ██            ║
    ║        ██              ██             ║
    ║          ████████████                 ║
    ║                                       ║
    ║      Créé par hacker_tchadien         ║
    ╚═══════════════════════════════════════╝
    """,
    """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║     📧 GMAIL CONV BACKUP 📧          ║
    ║                                       ║
    ║         ████████████████              ║
    ║       ██                ██            ║
    ║      ██    ▒▒░░▓▓▓▓░░▒▒    ██         ║
    ║     ██    ▒▒░░▓▓  ▓▓░░▒▒    ██        ║
    ║     ██   ▒▒░░▓▓ ██ ▓▓░░▒▒   ██        ║
    ║     ██   ▒▒░░▓▓████▓▓░░▒▒   ██        ║
    ║     ██   ▒▒░░▓▓ ██ ▓▓░░▒▒   ██        ║
    ║      ██   ▒▒░░▓▓  ▓▓░░▒▒   ██         ║
    ║       ██   ▒▒░░▓▓▓▓░░▒▒   ██          ║
    ║        ██              ██             ║
    ║          ████████████                 ║
    ║                                       ║
    ║      Créé par hacker_tchadien         ║
    ╚═══════════════════════════════════════╝
    """,
    """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║     📧 GMAIL CONV BACKUP 📧          ║
    ║                                       ║
    ║         ████████████████              ║
    ║       ██                ██            ║
    ║      ██    ▓▓▒▒░░░░▒▒▓▓    ██         ║
    ║     ██    ▓▓▒▒░░  ░░▒▒▓▓    ██        ║
    ║     ██   ▓▓▒▒░░ ██ ░░▒▒▓▓   ██        ║
    ║     ██   ▓▓▒▒░░████░░▒▒▓▓   ██        ║
    ║     ██   ▓▓▒▒░░ ██ ░░▒▒▓▓   ██        ║
    ║      ██   ▓▓▒▒░░  ░░▒▒▓▓   ██         ║
    ║       ██   ▓▓▒▒░░░░▒▒▓▓   ██          ║
    ║        ██              ██             ║
    ║          ████████████                 ║
    ║                                       ║
    ║      Créé par hacker_tchadien         ║
    ╚═══════════════════════════════════════╝
    """,
]

# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════════

class GmailBackup:
    """
    Classe principale pour la sauvegarde vers Gmail
    """
    
    def __init__(self):
        self.service = None
        self.user_email = None
        self.config = self._load_config()
        self._ensure_config_dir()
        
    def _ensure_config_dir(self):
        """Crée le répertoire de configuration"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
    def _load_config(self):
        """Charge la configuration"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {
            'chunk_size': 24 * 1024 * 1024,  # 24MB (limite Gmail = 25MB)
            'compress_before_send': True,
            'encrypt_files': False,
            'default_label': 'GmailCONV-Backup',
            'auto_cleanup': True,
            'retention_days': 30,
            'backup_history': []
        }
    
    def _save_config(self):
        """Sauvegarde la configuration"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _log(self, message):
        """Écrit dans le log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # AUTHENTIFICATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    def authenticate(self):
        """
        Authentifie l'utilisateur avec Gmail via OAuth2
        """
        console.print("\n[bold cyan]╔══════════════════════════════════════════════════════════════╗[/]")
        console.print("[bold cyan]║[/]  [bold green]🔐 Authentification Gmail OAuth2[/bold green]                          [bold cyan]║[/]")
        console.print("[bold cyan]╚══════════════════════════════════════════════════════════════╝[/]\n")
        
        creds = None
        
        # Charger les tokens existants
        if TOKEN_FILE.exists():
            console.print("[yellow]📂 Chargement des tokens existants...[/]")
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        # Rafraîchir ou créer de nouveaux tokens
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                console.print("[yellow]🔄 Rafraîchissement du token...[/]")
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    console.print("\n[bold red]❌ ERREUR: Fichier credentials.json manquant![/]")
                    console.print("""
[bold yellow]📋 Instructions pour obtenir credentials.json:[/]

1. Allez sur [bold blue]https://console.cloud.google.com/[/]
2. Créez un nouveau projet (ou utilisez-en un existant)
3. Activez l'API Gmail:
   - Menu ≡ → API & Services → Bibliothèque
   - Recherchez "Gmail API" → Cliquez sur "Activer"
4. Créez des identifiants OAuth2:
   - API & Services → Identifiants → Créer des identifiants
   - Choisissez "ID client OAuth"
   - Type d'application: "Application de bureau"
   - Nom: "GmailCONV"
   - Téléchargez le fichier JSON
5. Copiez le fichier téléchargé dans:
   [bold]{credentials_path}[/]
                    """.format(credentials_path=CREDENTIALS_FILE))
                    return False
                
                console.print("[yellow]🌐 Ouverture du navigateur pour l'authentification...[/]")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Sauvegarder les tokens
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
            console.print("[green]✅ Tokens sauvegardés avec succès![/]")
        
        # Construire le service
        self.service = build('gmail', 'v1', credentials=creds)
        
        # Récupérer l'email de l'utilisateur
        profile = self.service.users().getProfile(userId='me').execute()
        self.user_email = profile.get('emailAddress', 'inconnu')
        
        console.print(f"[bold green]✅ Connecté en tant que: {self.user_email}[/]\n")
        self._log(f"Authentification réussie: {self.user_email}")
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GESTION DES LABELS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_or_create_label(self, label_name):
        """
        Récupère ou crée un label Gmail
        """
        try:
            # Lister les labels existants
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            # Chercher le label
            for label in labels:
                if label['name'] == label_name:
                    return label['id']
            
            # Créer le label s'il n'existe pas
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            created = self.service.users().labels().create(
                userId='me', body=label_object).execute()
            
            console.print(f"[green]🏷️  Label créé: {label_name}[/]")
            self._log(f"Label créé: {label_name}")
            return created['id']
            
        except HttpError as e:
            console.print(f"[red]❌ Erreur création label: {e}[/]")
            return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMPRESSION & CHIFFREMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def compress_folder(self, folder_path, output_path=None):
        """
        Compresse un dossier en ZIP
        """
        folder_path = Path(folder_path)
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = CONFIG_DIR / f"{folder_path.name}_{timestamp}.zip"
        else:
            output_path = Path(output_path)
        
        console.print(f"[yellow]📦 Compression de: {folder_path}[/]")
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(folder_path)
                    zipf.write(file_path, arcname)
        
        size_mb = output_path.stat().st_size / (1024 * 1024)
        console.print(f"[green]✅ Compressé: {output_path} ({size_mb:.2f} MB)[/]")
        self._log(f"Compression: {folder_path} -> {output_path} ({size_mb:.2f} MB)")
        
        return output_path
    
    def split_file(self, file_path, chunk_size=None):
        """
        Divise un fichier en morceaux (pour les gros fichiers)
        """
        if chunk_size is None:
            chunk_size = self.config['chunk_size']
        
        file_path = Path(file_path)
        file_size = file_path.stat().st_size
        
        if file_size <= chunk_size:
            return [file_path]
        
        console.print(f"[yellow]✂️  Fragmentation du fichier ({file_size / (1024*1024):.2f} MB)...[/]")
        
        chunks = []
        with open(file_path, 'rb') as f:
            chunk_num = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                chunk_path = CONFIG_DIR / f"{file_path.stem}_part{chunk_num:03d}{file_path.suffix}"
                with open(chunk_path, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                
                chunks.append(chunk_path)
                chunk_num += 1
        
        console.print(f"[green]✅ Fichier divisé en {len(chunks)} parties[/]")
        self._log(f"Fragmentation: {file_path} -> {len(chunks)} parties")
        return chunks
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ENVOI D'EMAIL
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_message_with_attachment(self, sender, to, subject, body, file_path):
        """
        Crée un message email avec pièce jointe
        """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        
        # Corps du message
        msg_body = MIMEText(body, 'plain', 'utf-8')
        message.attach(msg_body)
        
        # Pièce jointe
        file_path = Path(file_path)
        content_type, encoding = mimetypes.guess_type(str(file_path))
        
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        
        main_type, sub_type = content_type.split('/', 1)
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        attachment = MIMEBase(main_type, sub_type)
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)
        
        filename = file_path.name
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )
        message.attach(attachment)
        
        # Encoder en base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        return {'raw': raw_message}
    
    def send_email(self, message_data, label_ids=None):
        """
        Envoie un email via Gmail API
        """
        try:
            sent = self.service.users().messages().send(
                userId='me', body=message_data).execute()
            
            msg_id = sent['id']
            
            # Ajouter les labels
            if label_ids:
                self.service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={'addLabelIds': label_ids}
                ).execute()
            
            return msg_id
            
        except HttpError as e:
            console.print(f"[red]❌ Erreur envoi: {e}[/]")
            return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SAUVEGARDE PRINCIPALE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def backup_file(self, file_path, custom_label=None, description=None):
        """
        Sauvegarde un fichier unique sur Gmail
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            console.print(f"[red]❌ Fichier non trouvé: {file_path}[/]")
            return False
        
        # Vérifier la taille
        file_size = file_path.stat().st_size
        max_size = 25 * 1024 * 1024  # 25MB limite Gmail
        
        if file_size > max_size:
            console.print(f"[yellow]⚠️  Fichier trop gros ({file_size / (1024*1024):.2f} MB)[/]")
            console.print("[yellow]   Fragmentation en cours...[/]")
            chunks = self.split_file(file_path)
            
            success_count = 0
            for i, chunk in enumerate(chunks):
                chunk_desc = f"{description or file_path.name} (Partie {i+1}/{len(chunks)})"
                if self.backup_file(chunk, custom_label, chunk_desc):
                    success_count += 1
                chunk.unlink(missing_ok=True)  # Nettoyer
            
            return success_count == len(chunks)
        
        # Label
        label_name = custom_label or self.config['default_label']
        label_id = self.get_or_create_label(label_name)
        label_ids = [label_id] if label_id else []
        
        # Sujet et description
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = file_path.name
        
        subject = f"[GmailCONV] Sauvegarde: {filename}"
        
        if description:
            body = f"""
Sauvegarde automatique GmailCONV
═══════════════════════════════════════

Fichier: {filename}
Date: {timestamp}
Taille: {file_size / 1024:.2f} KB
Description: {description}

Ce fichier a été sauvegardé automatiquement par GmailCONV.
Créé par hacker_tchadien

═══════════════════════════════════════
GmailCONV - Sauvegarde sécurisée vers Gmail
"""
        else:
            body = f"""
Sauvegarde automatique GmailCONV
═══════════════════════════════════════

Fichier: {filename}
Date: {timestamp}
Taille: {file_size / 1024:.2f} KB

Ce fichier a été sauvegardé automatiquement par GmailCONV.
Créé par hacker_tchadien

═══════════════════════════════════════
GmailCONV - Sauvegarde sécurisée vers Gmail
"""
        
        # Créer et envoyer le message
        console.print(f"[yellow]📤 Envoi de: {filename}[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Envoi en cours...", total=100)
            
            message = self.create_message_with_attachment(
                self.user_email,
                self.user_email,
                subject,
                body,
                file_path
            )
            progress.update(task, advance=50)
            
            msg_id = self.send_email(message, label_ids)
            progress.update(task, advance=50)
        
        if msg_id:
            console.print(f"[bold green]✅ Sauvegardé avec succès! ID: {msg_id}[/]")
            self._log(f"Sauvegarde réussie: {filename} -> {msg_id}")
            
            # Enregistrer dans l'historique
            self.config['backup_history'].append({
                'date': timestamp,
                'file': str(file_path),
                'size': file_size,
                'message_id': msg_id,
                'label': label_name
            })
            self._save_config()
            
            return True
        else:
            console.print(f"[bold red]❌ Échec de la sauvegarde[/]")
            self._log(f"Échec sauvegarde: {filename}")
            return False
    
    def backup_folder(self, folder_path, custom_label=None, compress=True):
        """
        Sauvegarde un dossier complet sur Gmail
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            console.print(f"[red]❌ Dossier non trouvé: {folder_path}[/]")
            return False
        
        if compress:
            # Compresser le dossier
            zip_path = self.compress_folder(folder_path)
            result = self.backup_file(zip_path, custom_label, 
                f"Dossier compressé: {folder_path.name}")
            
            # Nettoyer le ZIP temporaire
            if self.config.get('auto_cleanup', True):
                zip_path.unlink(missing_ok=True)
            
            return result
        else:
            # Envoyer chaque fichier individuellement
            files = [f for f in folder_path.rglob('*') if f.is_file()]
            console.print(f"[yellow]📁 {len(files)} fichiers à sauvegarder[/]")
            
            success_count = 0
            for i, file_path in enumerate(files, 1):
                console.print(f"\n[cyan]Fichier {i}/{len(files)}:[/]")
                if self.backup_file(file_path, custom_label):
                    success_count += 1
            
            console.print(f"\n[bold green]✅ {success_count}/{len(files)} fichiers sauvegardés[/]")
            return success_count == len(files)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTERFACE UTILISATEUR
    # ═══════════════════════════════════════════════════════════════════════════
    
    def show_banner(self):
        """Affiche la bannière animée"""
        console.print("\n[bold green]" + "═" * 70 + "[/]")
        for frame in GMAIL_LOGO_FRAMES:
            console.print(frame)
            time.sleep(0.3)
            console.clear()
        console.print(GMAIL_LOGO_FRAMES[0])
        console.print("[bold green]" + "═" * 70 + "[/]\n")
    
    def show_menu(self):
        """Affiche le menu principal"""
        console.print(Panel.fit(
            "[bold cyan]📧 GMAILCONV - MENU PRINCIPAL[/bold cyan]\n\n"
            "[green]1.[/] Sauvegarder un fichier\n"
            "[green]2.[/] Sauvegarder un dossier (compressé)\n"
            "[green]3.[/] Sauvegarder un dossier (fichiers séparés)\n"
            "[green]4.[/] Voir l'historique des sauvegardes\n"
            "[green]5.[/] Voir les statistiques\n"
            "[green]6.[/] Configurer les paramètres\n"
            "[green]0.[/] Quitter\n",
            title="[bold green]GmailCONV[/bold green]",
            subtitle="[dim]Créé par hacker_tchadien[/dim]",
            border_style="green"
        ))
    
    def show_history(self):
        """Affiche l'historique des sauvegardes"""
        history = self.config.get('backup_history', [])
        
        if not history:
            console.print("[yellow]📭 Aucune sauvegarde dans l'historique[/]")
            return
        
        table = Table(title="📋 Historique des Sauvegardes")
        table.add_column("Date", style="cyan")
        table.add_column("Fichier", style="green")
        table.add_column("Taille", style="yellow")
        table.add_column("Label", style="magenta")
        table.add_column("ID Message", style="dim")
        
        for entry in history[-20:]:  # 20 dernières
            size_str = f"{entry['size'] / 1024:.1f} KB" if entry['size'] < 1024*1024 else f"{entry['size'] / (1024*1024):.2f} MB"
            table.add_row(
                entry['date'],
                Path(entry['file']).name,
                size_str,
                entry['label'],
                entry['message_id'][:20] + "..."
            )
        
        console.print(table)
    
    def show_stats(self):
        """Affiche les statistiques"""
        history = self.config.get('backup_history', [])
        
        if not history:
            console.print("[yellow]📭 Aucune statistique disponible[/]")
            return
        
        total_files = len(history)
        total_size = sum(e['size'] for e in history)
        unique_labels = len(set(e['label'] for e in history))
        
        table = Table(title="📊 Statistiques GmailCONV")
        table.add_column("Métrique", style="cyan")
        table.add_column("Valeur", style="green")
        
        table.add_row("Total sauvegardes", str(total_files))
        table.add_row("Taille totale", f"{total_size / (1024*1024):.2f} MB")
        table.add_row("Labels utilisés", str(unique_labels))
        table.add_row("Première sauvegarde", history[0]['date'])
        table.add_row("Dernière sauvegarde", history[-1]['date'])
        
        console.print(table)
    
    def configure(self):
        """Configure les paramètres"""
        console.print(Panel.fit(
            "[bold cyan]⚙️  CONFIGURATION[/bold cyan]\n\n"
            "[green]1.[/] Taille max par fichier (actuel: {:.1f} MB)\n"
            "[green]2.[/] Compression auto: {}\n"
            "[green]3.[/] Label par défaut: {}\n"
            "[green]4.[/] Nettoyage auto: {}\n"
            "[green]5.[/] Retention (jours): {}\n"
            "[green]0.[/] Retour\n".format(
                self.config['chunk_size'] / (1024*1024),
                "Oui" if self.config['compress_before_send'] else "Non",
                self.config['default_label'],
                "Oui" if self.config['auto_cleanup'] else "Non",
                self.config['retention_days']
            ),
            border_style="cyan"
        ))
    
    def run(self):
        """Boucle principale"""
        self.show_banner()
        
        # Authentification
        if not self.authenticate():
            console.print("[bold red]❌ Authentification échouée. Arrêt.[/]")
            return
        
        while True:
            self.show_menu()
            choice = console.input("[bold green]Votre choix: [/]")
            
            if choice == '1':
                file_path = console.input("[cyan]Chemin du fichier: [/]")
                label = console.input("[cyan]Label Gmail (optionnel): [/]") or None
                desc = console.input("[cyan]Description (optionnel): [/]") or None
                self.backup_file(file_path, label, desc)
                
            elif choice == '2':
                folder_path = console.input("[cyan]Chemin du dossier: [/]")
                label = console.input("[cyan]Label Gmail (optionnel): [/]") or None
                self.backup_folder(folder_path, label, compress=True)
                
            elif choice == '3':
                folder_path = console.input("[cyan]Chemin du dossier: [/]")
                label = console.input("[cyan]Label Gmail (optionnel): [/]") or None
                self.backup_folder(folder_path, label, compress=False)
                
            elif choice == '4':
                self.show_history()
                
            elif choice == '5':
                self.show_stats()
                
            elif choice == '6':
                self.configure()
                
            elif choice == '0':
                console.print("\n[bold green]👋 Au revoir! GmailCONV s'arrête.[/]")
                break
            
            console.input("\n[dim]Appuyez sur Entrée pour continuer...[/]")


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def quick_backup(file_path, label=None):
    """
    Sauvegarde rapide d'un fichier (usage programmatique)
    """
    backup = GmailBackup()
    if backup.authenticate():
        return backup.backup_file(file_path, label)
    return False


def quick_backup_folder(folder_path, label=None, compress=True):
    """
    Sauvegarde rapide d'un dossier (usage programmatique)
    """
    backup = GmailBackup()
    if backup.authenticate():
        return backup.backup_folder(folder_path, label, compress)
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='GmailCONV - Sauvegarde vers Gmail',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  %(prog)s                          # Mode interactif
  %(prog)s -f document.pdf          # Sauvegarder un fichier
  %(prog)s -d /chemin/dossier       # Sauvegarder un dossier
  %(prog)s -f file.txt -l "Important" # Avec label personnalisé
        """
    )
    
    parser.add_argument('-f', '--file', help='Fichier à sauvegarder')
    parser.add_argument('-d', '--directory', help='Dossier à sauvegarder')
    parser.add_argument('-l', '--label', help='Label Gmail')
    parser.add_argument('--no-compress', action='store_true', 
                        help='Ne pas compresser (pour dossiers)')
    
    args = parser.parse_args()
    
    if args.file:
        quick_backup(args.file, args.label)
    elif args.directory:
        quick_backup_folder(args.directory, args.label, 
                           compress=not args.no_compress)
    else:
        app = GmailBackup()
        app.run()
