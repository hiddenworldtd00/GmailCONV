#!/usr/bin/env python3
"""
Script de configuration GmailCONV
Créé par hacker_tchadien
"""

import os
import sys
import json

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def setup_credentials():
    """Guide l'utilisateur pour configurer les credentials Gmail"""
    console.print(Panel.fit(
        Text("🔧 CONFIGURATION GmailCONV", style="bold green"),
        border_style="green"
    ))
    
    console.print("""
[bold cyan]Étape 1: Créer un projet Google Cloud[/bold cyan]
1. Allez sur [link]https://console.cloud.google.com/[/link]
2. Créez un nouveau projet (ex: "GmailCONV")
3. Activez l'API Gmail:
   - Menu ≡ → APIs & Services → Library
   - Cherchez "Gmail API"
   - Cliquez sur "Enable"

[bold cyan]Étape 2: Créer les credentials OAuth2[/bold cyan]
1. Menu ≡ → APIs & Services → Credentials
2. Cliquez "Create Credentials" → "OAuth client ID"
3. Configurez l'écran de consentement:
   - Type: "External"
   - Remplissez les informations basiques
4. Créez le client ID:
   - Type d'application: "Desktop app"
   - Nom: "GmailCONV"
5. Téléchargez le fichier JSON

[bold cyan]Étape 3: Placer le fichier credentials[/bold cyan]
""")
    
    # Demander le chemin du fichier credentials
    creds_path = console.input("[yellow]Chemin du fichier credentials.json téléchargé: [/yellow]").strip()
    
    if not os.path.exists(creds_path):
        console.print("[red]❌ Fichier non trouvé![/red]")
        return False
    
    # Copier dans le dossier GmailCONV
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
    
    try:
        import shutil
        shutil.copy2(creds_path, dest)
        console.print(f"[green]✅ Credentials copiés vers: {dest}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Erreur: {e}[/red]")
        return False
    
    # Créer le fichier de configuration
    config = {
        'setup_complete': True,
        'credentials_path': dest,
        'default_email': '',
        'backup_folder': os.path.expanduser('~/Documents'),
    }
    
    config_path = os.path.join(os.path.dirname(dest), 'settings.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    console.print(f"[green]✅ Configuration sauvegardée dans: {config_path}[/green]")
    
    console.print("""
[bold green]✅ Configuration terminée![/bold green]

Vous pouvez maintenant utiliser GmailCONV:
  [cyan]python gmail_backup.py --help[/cyan]

Pour votre première sauvegarde:
  [cyan]python gmail_backup.py --folder ~/Documents --email votre.email@gmail.com[/cyan]
""")
    
    return True

def check_setup():
    """Vérifie si la configuration est complète"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    checks = {
        'credentials.json': os.path.exists(os.path.join(base_dir, 'credentials.json')),
        'settings.json': os.path.exists(os.path.join(base_dir, 'settings.json')),
    }
    
    console.print("\n[bold]Vérification de la configuration:[/bold]")
    for item, exists in checks.items():
        status = "[green]✅[/green]" if exists else "[red]❌[/red]"
        console.print(f"  {status} {item}")
    
    return all(checks.values())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        if check_setup():
            console.print("\n[green]✅ Configuration complète![/green]")
            sys.exit(0)
        else:
            console.print("\n[yellow]⚠️ Configuration incomplète. Lancez: python setup.py[/yellow]")
            sys.exit(1)
    else:
        setup_credentials()
