# This class stores ANSI color codes for making terminal output colorful
class Colors:
    Reset = "\033[0m"
    BrightGreen = "\033[1;92m"
    BrightBlue = "\033[1;94m"
    BrightYellow = "\033[1;93m"
    BrightMagenta = "\033[1;95m"
    BrightCyan = "\033[1;96m"
    BrightRed = "\033[1;91m"
    BrightWhite = "\033[1;97m"

# This function displays a colored banner with tool info and credits
def display_banner():
    banner = r"""
      __        _______ ____   ____    _    ____ _____ _   _ ____  _____ 
      \ \      / / ____| __ ) / ___|  / \  |  _ \_   _| | | |  _ \| ____|
       \ \ /\ / /|  _| |  _ \| |     / _ \ | |_) || | | | | | |_) |  _|  
        \ V  V / | |___| |_) | |___ / ___ \|  __/ | | | |_| |  _ <| |___ 
         \_/\_/  |_____|____/ \____/_/   \_\_|    |_|  \___/|_| \_\_____|
    """

    # Split the banner into lines so each can be printed in a different color
    lines = banner.strip().split('\n')

    # We'll cycle through these colors line by line
    colored_lines = []
    colors = [
        Colors.BrightGreen,
        Colors.BrightBlue,
        Colors.BrightYellow,
        Colors.BrightMagenta,
        Colors.BrightCyan,
        Colors.BrightRed
    ]

    # Loop through each line and apply a color from the list
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        colored_lines.append(f"{color}{line}{Colors.Reset}")

    # Print the final banner with color effects
    print("\n" + "\n".join(colored_lines))

    # Print developer name in yellow
    print(f"\n{Colors.BrightYellow}                            Developer: Dracky Jr {Colors.Reset}")

    # Tool description and bottom line
    print(f"\n{Colors.BrightCyan}* Advanced OSINT Tool {Colors.Reset}")
    print(f"{Colors.BrightGreen}─" * 80 + Colors.Reset)

