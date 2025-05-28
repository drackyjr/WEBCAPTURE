class Colors:
    BrightRed = "\\033[1;91m"
    BrightGreen = "\\033[1;92m"
    BrightYellow = "\\033[1;93m"
    BrightWhite = "\\033[1;97m"
    Cyan = "\\033[1;96m"
    Reset = "\\033[0m"

def display_banner():
    print(f"{Colors.BrightGreen}")
    print(r"""
      __        _______ ____   ____    _    ____ _____ _   _ ____  _____ 
      \ \      / / ____| __ ) / ___|  / \  |  _ \_   _| | | |  _ \| ____|
       \ \ /\ / /|  _| |  _ \| |     / _ \ | |_) || | | | | | |_) |  _|  
        \ V  V / | |___| |_) | |___ / ___ \|  __/ | | | |_| |  _ <| |___ 
         \_/\_/  |_____|____/ \____/_/   \_\_|    |_|  \___/|_| \_\_____|


                            Developer: DRACKY JR
    """)
    print(f"{Colors.Cyan}* Advanced OSINT Tool {Colors.Reset}")

