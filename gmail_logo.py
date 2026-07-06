#!/usr/bin/env python3
"""
Logo Gmail animé ASCII pour GmailCONV
Créé par hacker_tchadien
"""

import sys
import time
import threading

class GmailLogoAnimator:
    """Anime le logo Gmail en ASCII art"""
    
    LOGO_FRAMES = [
        [
            "    ██████╗  ██████╗  ██████╗  ██████╗ ██╗     ███████╗",
            "   ██╔════╝ ██╔════╝ ██╔═══██╗██╔════╝ ██║     ██╔════╝",
            "   ██║  ███╗██║  ███╗██║   ██║██║  ███╗██║     █████╗  ",
            "   ██║   ██║██║   ██║██║   ██║██║   ██║██║     ██╔══╝  ",
            "   ╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║     ",
            "    ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝     ",
        ],
        [
            "   ▄██████▄  ▄██████▄  ▄██████▄  ▄██████▄  ██         ",
            "  ███    ███ ███    ███ ███   ███ ███    ███ ██         ",
            "  ███    █▀  ███    █▀  ███   ███ ███    █▀  ██         ",
            " ▄███        ███        ███   ███ ███        ██         ",
            "▀▀███ ████▄  ███  ███▄  ███   ███ ███  ███▄  ██         ",
            "  ███    ███ ███    ███ ███   ███ ███    ███ ██         ",
            "  ███    ███ ███    ███ ███   ███ ███    ███ ██         ",
            "  ████████▀   ▀██████▀   ▀██████▀   ▀██████▀  ████████  ",
        ],
    ]
    
    MAIL_FRAMES = [
        [
            "    ┌─────────────────────────────┐",
            "    │  📧                         │",
            "    │      ╱╲                     │",
            "    │     ╱  ╲                    │",
            "    │    ╱    ╲                   │",
            "    │   ╱──────╲                  │",
            "    │  ╱        ╲                 │",
            "    │ ╱          ╲                │",
            "    └─────────────────────────────┘",
        ],
        [
            "    ┌─────────────────────────────┐",
            "    │                             │",
            "    │      ╱╲    📧               │",
            "    │     ╱  ╲                    │",
            "    │    ╱    ╲                   │",
            "    │   ╱──────╲                  │",
            "    │  ╱        ╲                 │",
            "    │ ╱          ╲                │",
            "    └─────────────────────────────┘",
        ],
        [
            "    ┌─────────────────────────────┐",
            "    │                             │",
            "    │      ╱╲                     │",
            "    │     ╱  ╲   📧               │",
            "    │    ╱    ╲                   │",
            "    │   ╱──────╲                  │",
            "    │  ╱        ╲                 │",
            "    │ ╱          ╲                │",
            "    └─────────────────────────────┘",
        ],
        [
            "    ┌─────────────────────────────┐",
            "    │                             │",
            "    │      ╱╲                     │",
            "    │     ╱  ╲                    │",
            "    │    ╱    ╲  📧               │",
            "    │   ╱──────╲                  │",
            "    │  ╱        ╲                 │",
            "    │ ╱          ╲                │",
            "    └─────────────────────────────┘",
        ],
    ]
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.frame_index = 0
    
    def clear_screen(self):
        """Nettoie l'écran"""
        print('\033[2J\033[H', end='')
    
    def hide_cursor(self):
        """Cache le curseur"""
        print('\033[?25l', end='')
    
    def show_cursor(self):
        """Affiche le curseur"""
        print('\033[?25h', end='')
    
    def print_gmail_logo(self, color=True):
        """Affiche le logo Gmail"""
        RED = '\033[91m' if color else ''
        WHITE = '\033[97m' if color else ''
        BLUE = '\033[94m' if color else ''
        YELLOW = '\033[93m' if color else ''
        GREEN = '\033[92m' if color else ''
        RESET = '\033[0m' if color else ''
        BOLD = '\033[1m' if color else ''
        
        logo = [
            "",
            f"{RED}        ▄███████▄{RESET}    {WHITE}▄████████{RESET}    {BLUE}▄████████{RESET}    {YELLOW}▄█        ██████████{RESET}   {GREEN}▄████████{RESET}  {WHITE}▄█{RESET}        ",
            f"{RED}       ███    ███{RESET}   {WHITE}███    ███{RESET}   {BLUE}███    ███{RESET}   {YELLOW}███       ███░░░░░░███{RESET}  {GREEN}███    ███{RESET} {WHITE}███{RESET}        ",
            f"{RED}       ███    ███{RESET}   {WHITE}███    █▀{RESET}    {BLUE}███    █▀{RESET}    {YELLOW}███       ░███    ░███{RESET}  {GREEN}███    █▀{RESET}  {WHITE}███{RESET}        ",
            f"{RED}       ███    ███{RESET}  {WHITE}▄███▄▄▄{RESET}      {BLUE}▄███▄▄▄{RESET}      {YELLOW}███       ░███████████{RESET}  {GREEN}▄███▄▄▄{RESET}     {WHITE}███{RESET}        ",
            f"{RED}     ▀█████████▀{RESET}  {WHITE}▀▀███▀▀▀{RESET}      {BLUE}▀▀███▀▀▀{RESET}      {YELLOW}███       ░███░░░░░░███{RESET} {GREEN}▀▀███▀▀▀{RESET}     {WHITE}███{RESET}        ",
            f"{RED}       ███{RESET}         {WHITE}███    █▄{RESET}     {BLUE}███    █▄{RESET}    {YELLOW}███       ░███    ░███{RESET}  {GREEN}███    █▄{RESET}  {WHITE}███{RESET}        ",
            f"{RED}       ███{RESET}         {WHITE}███    ███{RESET}   {BLUE}███    ███{RESET}   {YELLOW}███▌    ▄ ░███    ░███{RESET}  {GREEN}███    ███{RESET} {WHITE}███▌    ▄{RESET} ",
            f"{RED}      ▄████▀{RESET}       {WHITE}██████████{RESET}  {BLUE}██████████{RESET}  {YELLOW}█████▄▄██{RESET} {YELLOW}████████████{RESET}  {GREEN}██████████{RESET} {WHITE}█████▄▄██{RESET}",
            f"{YELLOW}                                                          ▀{RESET}                          {WHITE}▀{RESET}        ",
            "",
            f"{BOLD}{WHITE}              ╔═══════════════════════════════════════════════════════════════╗{RESET}",
            f"{BOLD}{WHITE}              ║{RESET}   {GREEN}📧  GMAIL CONV - Sauvegarde Cloud par Gmail{RESET}              {BOLD}{WHITE}║{RESET}",
            f"{BOLD}{WHITE}              ║{RESET}   {YELLOW}Créé par hacker_tchadien pour la communauté Tchadienne{RESET}   {BOLD}{WHITE}║{RESET}",
            f"{BOLD}{WHITE}              ╚═══════════════════════════════════════════════════════════════╝{RESET}",
            "",
        ]
        
        for line in logo:
            print(line)
    
    def animate_sending(self, duration=3):
        """Anime l'envoi d'un email"""
        self.hide_cursor()
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                self.clear_screen()
                self.print_gmail_logo()
                
                # Afficher l'enveloppe animée
                frame = self.MAIL_FRAMES[self.frame_index % len(self.MAIL_FRAMES)]
                for line in frame:
                    print(f"                    {line}")
                
                print("")
                print(f"                    {YELLOW}📤 Envoi en cours...{RESET}")
                print(f"                    {GREEN}▓{'░' * (19 - self.frame_index % 20)}{RESET}")
                
                self.frame_index += 1
                time.sleep(0.3)
                
        finally:
            self.show_cursor()
    
    def animate_loading(self, message="Chargement", duration=2):
        """Anime un chargement"""
        self.hide_cursor()
        start_time = time.time()
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        
        try:
            i = 0
            while time.time() - start_time < duration:
                self.clear_screen()
                self.print_gmail_logo()
                
                print(f"\n                    {BLUE}{frames[i % len(frames)]}{RESET}  {WHITE}{message}...{RESET}")
                print(f"                    {GREEN}{'▓' * (i % 20)}{'░' * (20 - i % 20)}{RESET}")
                
                i += 1
                time.sleep(0.1)
                
        finally:
            self.show_cursor()
    
    def print_success(self):
        """Affiche le succès"""
        self.clear_screen()
        self.print_gmail_logo()
        
        GREEN = '\033[92m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
        
        print(f"\n                    {GREEN}✅ Sauvegarde terminée avec succès!{RESET}")
        print(f"                    {WHITE}📧 Vos fichiers sont en sécurité sur Gmail{RESET}")
        print("")
    
    def print_error(self, error_msg):
        """Affiche une erreur"""
        self.clear_screen()
        self.print_gmail_logo()
        
        RED = '\033[91m'
        WHITE = '\033[97m'
        RESET = '\033[0m'
        
        print(f"\n                    {RED}❌ Erreur: {error_msg}{RESET}")
        print(f"                    {WHITE}💡 Vérifiez votre connexion et réessayez{RESET}")
        print("")


def main():
    """Démo du logo animé"""
    animator = GmailLogoAnimator()
    
    # Animation de chargement
    animator.animate_loading("Connexion à Gmail", 2)
    
    # Animation d'envoi
    animator.animate_sending(3)
    
    # Succès
    animator.print_success()


if __name__ == "__main__":
    main()
