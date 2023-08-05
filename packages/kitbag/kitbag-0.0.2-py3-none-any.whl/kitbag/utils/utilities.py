# Python module holding utility functions for plotting
from PIL import Image
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from ..utils.colors import team_colors
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

class FontManager:
    """Utility to load fonts for matplotlib.
    The FontManager is taken from the mplsoccer package by Andy Rowlinson (@numberstorm).
    Parameters
    ----------
    url : str, default is the url for SuperGroteskComp.ttf
        Can really be any .ttf file, but probably looks like
        'https://github.com/FC-Nordsjaelland/kitbag/blob/main/utils/fonts/SuperGroteskComp.ttf?raw=True'
        Note 1: make sure the ?raw=true is at the end.
        Note 2: urls like 'https://raw.githubusercontent.com/FC-Nordsjaelland/kitbag/blob/main/utils/fonts/SuperGroteskComp.ttf'
                allow Cross-Origin Resource Sharing, and work in browser environments
                based on PyOdide (e.g. JupyterLite). Those urls don't need the ?raw=true at the end
    Examples
    --------
    >>> from kitbag.utils.utilities import FontManager
    >>> import matplotlib.pyplot as plt
    >>> font_url = 'https://github.com/FC-Nordsjaelland/kitbag/blob/main/utils/fonts/SuperGroteskComp.ttf?raw=True'
    >>> fm = FontManager(url=font_url)
    >>> fig, ax = plt.subplots()
    >>> ax.text(x=0.5, y=0.5, s="Good content.", fontproperties=fm.prop, size=30)
    """

    def __init__(self,
                 url=('https://github.com/FC-Nordsjaelland/kitbag/blob/main/utils/fonts/SuperGroteskComp.ttf?raw=True')):
        self.url = url
        with NamedTemporaryFile(delete=False, suffix=".ttf") as temp_file:
            temp_file.write(urlopen(self.url).read())
            self._prop = fm.FontProperties(fname=temp_file.name)

    @property
    def prop(self):
        """Get matplotlib.font_manager.FontProperties object that sets the custom font."""
        return self._prop

    def __repr__(self):
        return f'{self.__class__.__name__}(font_url={self.url})'
    
    
def shift_row_to_bottom(df, index_to_shift):
    idx = [i for i in df.index if i!=index_to_shift]
    return df.loc[[index_to_shift] + idx]

def add_banner(fig, title, team):
    fig_width, fig_height = fig.get_size_inches()
    
    # title
    fig.text(0.11, 0.975, s=title, fontsize=28, fontweight="bold")
    
    # add banner and image
    # banner
    fig.patches.extend([plt.Rectangle((0.05, 0.95), 0.9, 0.08,
                                      fill=True, color=team_colors[team], alpha=0.85, zorder=-1000,
                                      transform=fig.transFigure, figure=fig)])
    # text
    team_text = team.replace(" ", "\n")
    fig.text(0.74, 0.99, s=team_text, fontsize=22, fontweight="bold", va="center")
    
    # image
    # logo = Image.open("../utils/logos/FCN Logos/FCN Logo R&Y.png")
    # ax_image_home = fig.add_axes((0.85, 0.93, 0.125, 0.125))
    # ax_image_home.axis('off')  # axis off so no labels/ ticks
    # ax_image_home.imshow(logo)

# def load_fonts(font_path):
#     for x in os.listdir(font_path):
#         for y in os.listdir(f"{font_path}/{x}"):
#             if y.split(".")[-1] == "ttf":
#                 fm.fontManager.addfont(f"{font_path}/{x}/{y}")
#                 try:
#                     fm.FontProperties(weight=y.split("-")[-1].split(".")[0].lower(), fname=y)
#                     print(f"Added font {y}")
#                 except Exception as e:
#                     print(f"Font {y} could not be added.")
#                     continue

# font_path = "fonts"

def shift_row_to_bottom(df, index_to_shift):
    idx = [i for i in df.index if i!=index_to_shift]
    return df.loc[[index_to_shift] + idx]
