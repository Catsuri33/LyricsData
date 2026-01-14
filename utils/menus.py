from colorama import Fore, Style
import sys

from utils.download_lyrics import download_lyrics

def _print_header() -> None:
    header = f"""
        {Fore.CYAN}{Style.BRIGHT}
        ╔═════════════════════════════════════════════════════════╗
        ║               🎵  Lyrics Downloader  🎵               ║
        ╚═════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}
        """
    print(header)


def _prompt(message: str, *, required: bool = False) -> str:
    while True:
        answer = input(message).strip()
        if answer or not required:
            return answer
        print(f"{Fore.RED}Ce champ est obligatoire, veuillez entrer une valeur.{Style.RESET_ALL}")


def download_menu() -> None:
    _print_header()
    print(f"{Fore.YELLOW}{Style.BRIGHT}Veuillez choisir une option :{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Entrer les informations de la piste")
    print(f"  {Fore.RED}[2]{Style.RESET_ALL} Quitter")

    choice = _prompt("\nVotre choix (1/2) : ", required=True)

    if choice == "1":
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}--- Saisie des métadonnées ---{Style.RESET_ALL}")

        artist = _prompt("Nom de l'artiste (obligatoire) : ", required=True)
        album = _prompt("Nom de l'album (optionnel)   : ")
        track = _prompt("Titre du morceau (optionnel) : ")

        try:
            download_lyrics(
                artist=artist,
                track=track or "",
                album=album or ""
            )
            print(f"{Fore.GREEN}\n✅  Téléchargement terminé pour '{artist}'{Style.RESET_ALL}")
        except Exception as exc:
            print(f"{Fore.RED}\n❌  Erreur pendant le téléchargement : {exc}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Appuyez sur Entrée pour revenir au menu…{Style.RESET_ALL}")

    elif choice == "2":
        print(f"\n{Fore.BLUE}Au revoir !{Style.RESET_ALL}")
        sys.exit(0)

    else:
        print(f"{Fore.RED}Choix invalide ! Veuillez saisir 1 ou 2.{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Appuyez sur Entrée pour réessayer…{Style.RESET_ALL}")