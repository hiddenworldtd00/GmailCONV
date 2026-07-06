"""
Configuration GmailCONV
Créé par hacker_tchadien
"""

# Scopes Gmail API
GMAIL_SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.readonly'
]

# Fichiers de credentials
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

# Configuration sauvegarde
BACKUP_CONFIG = {
    'max_attachment_size': 24 * 1024 * 1024,  # 24 Mo (limite Gmail)
    'chunk_size': 256 * 1024,  # 256 Ko
    'max_retries': 3,
    'retry_delay': 2,  # secondes
    'batch_size': 50,  # fichiers par batch
}

# Types de fichiers supportés
SUPPORTED_TYPES = {
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
    'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.sql'],
    'data': ['.json', '.xml', '.csv', '.xls', '.xlsx', '.db', '.sqlite'],
}

# Extensions à exclure (risque sécurité)
EXCLUDED_EXTENSIONS = [
    '.exe', '.bat', '.cmd', '.sh', '.msi', '.dll', '.sys',
    '.com', '.scr', '.vbs', '.js', '.jar', '.apk', '.ipa'
]

# Labels Gmail pour organisation
GMAIL_LABELS = {
    'backup': 'GmailCONV/Backup',
    'documents': 'GmailCONV/Documents',
    'images': 'GmailCONV/Images',
    'videos': 'GmailCONV/Videos',
    'audio': 'GmailCONV/Audio',
    'archives': 'GmailCONV/Archives',
    'code': 'GmailCONV/Code',
    'data': 'GmailCONV/Data',
    'large': 'GmailCONV/Large-Files',
    'encrypted': 'GmailCONV/Encrypted',
}

# Messages
MESSAGES = {
    'fr': {
        'welcome': 'Bienvenue dans GmailCONV',
        'auth_required': 'Authentification Gmail requise',
        'backup_started': 'Sauvegarde démarrée',
        'backup_complete': 'Sauvegarde terminée',
        'error': 'Erreur',
        'success': 'Succès',
        'warning': 'Attention',
    }
}
