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
  __          __  _     ______      _                  _             
  \ \        / / | |   |  ____|    | |                | |            
   \ \  /\  / /__| |__ | |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __ 
    \ \/  \/ / _ \ '_ \|  __| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|
     \  /\  /  __/ |_) | |____ >  <| |_| | | (_| | (__| || (_) | |   
      \/  \/ \___|_.__/|______/_/\_\\__|_|  \__,_|\___|\__\___/|_|   

                            Developer: YourNameHere
    """)
    print(f"{Colors.Cyan}* Advanced OSINT Tool {Colors.Reset}")

