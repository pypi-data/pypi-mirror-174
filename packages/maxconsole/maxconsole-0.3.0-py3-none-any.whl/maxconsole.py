from gettext import install
from rich.console import Console
from rich.theme import Theme
from rich.traceback import install as install_traceback

__version__ = "0.3.0"

def get_theme() -> Theme:
    # . Hex Colors
    magenta = "#ff00ff"  #               #ff00ff
    purple = "#af00ff"  #                #af00ff
    blue_violet = "#5f00ff"  #           #5f00ff
    blue = "#0000ff"  #                  #0000ff
    cornflower_blue = "#249df1"  #       #249df1
    cyan = "#00ffff"  #                  #00ffff
    green = "#00ff00"  #                 #00ff00
    yellow = "#ffff00"  #                #ffff00
    orange = "#ff8800"  #                #ff8800
    red = "#ff0000"  #                   #ff0000

    # . Hex Tints
    white = "#ffffff"  #                 #ffffff
    light_grey = "#e2e2e2"  #            #e2e2e2
    grey = "#808080"  #                  #808080
    dark_grey = "#2e2e2e"  #             #2e2e2e
    black = "#000000"  #                 #000000


    theme_dict = {
        "magenta": "#ff00ff",  #         #ff00ff
        "purple": "#af00ff",  # P        #af00ff
        "blue_violet": "#5f00ff",  #     #5f00ff
        "blue": "bold #0000FF",  #       #0000ff
        "cornflower_blue": "#249df1",  # #249df1
        "cyan": "#00ffff",  #            #00ffff
        "green": "#00ff00",  #           #00ff00
        "yellow": "#ffff00",  #          #ffff00
        "orange": "#ff8800",  #          #ff8800
        "red": "#ff0000",  #             #ff0000
        "white": "#ffffff",  #           #ffffff
        "light_grey": "#e2e2e2",  #      #e2e2e2
        "grey": "#808080",  #            #808080
        "dark_grey": "#2e2e2e",  #       #2e2e2e
        "black": "#000000",  #           #000000
        "debug": "bold bright_cyan",  #    #00ffff
        "info": "bold cornflower_blue",  # #249df1
        "success": "bold bright_green",  # #00ff00
        "warning": "bold bright_yellow",  ##ffff00
        "error": "bold orange1",  #        #ff8800
        "critical": "bold reverse red",  # #ff0000
        "value": "bold bright_white",  #   #ffffff
        "title": "bold purple",  #         #af00ff
        "key": "italic magenta",  #        #ff00ff
        "lines": "blue_violet",  #         #5f00ff
    }
    theme = Theme(theme_dict)
    return theme

def get_console(theme: Theme) -> Console:
    if not theme:
        theme = get_theme()
    console = Console(theme=theme, color_system="truecolor")
    install_traceback(console=console, show_locals=True)
    return console

if __name__ == "__main__":
    theme = get_theme()
    console = get_console(theme)
