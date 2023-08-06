import re
import os
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
from highlight_text import fig_text

from ..utils.colors import grey, red, green, blue, yellow
from ..utils.utilities import add_banner

def plot_physical_volume(df, title, team):
    """
    Parameters:
        df (DataFrame): DataFrame with athlete and position as multiindex and metrics as columns
        title (str): Title of the bar chart
        team (str): Name of the team the bar chart is created for
        
    Returns:
        bar chart (mpl figure): A bar chart
        
    Example:
    """
    
    colors = {"Avg. Team": grey, "Centre Back": blue, "Midfielder": yellow,
              "Full Back": green, "Attacker": red}
    
    positions_plot = df.index.get_level_values('position_name').unique()
    cols = df.columns
    header_cols = [col.replace("(", "\n"+"(", 1) for col in cols]

    height_ratios = [1 for _ in range(len(positions_plot)-1)]
    height_ratios.insert(0, 0.15)
    
    fig, all_axes = plt.subplots(figsize=(14, 14),
                                 nrows=len(positions_plot), ncols=len(cols),
                                 facecolor=(1, 1, 1), gridspec_kw={'height_ratios': height_ratios})
    
    for i, axes in enumerate(all_axes):
        df_pos = df.query(f'position_name == "{positions_plot[i]}"')
        for j, ax in enumerate(axes):
            players = df_pos.index.get_level_values('athlete_name')
            y_pos = np.arange(len(df_pos))
            
            all_axes[i][j].set_xlim(0, max(df[cols[j]]))

            # plot bars
            bars = all_axes[i][j].barh(y_pos, df_pos[cols[j]], alpha=0.7, edgecolor="k",
                                        color=colors[positions_plot[i]])

            # change color of avg. position bars
            for k in range(len(bars)):
                if players[k] == f"Åvg. {positions_plot[i]}":
                    bars[k].set_color("#3C4043")
            
            # add reference line on åvg. position
            if positions_plot[i] != "Avg. Team":
                ax.axvline(df_pos[cols[j]].values[-1], ls="--", alpha=0.6, color="k")
            
            all_axes[i][j].invert_yaxis()  # labels read top-to-bottom

            # label for value with annotation
            all_axes[i][j].bar_label(bars, fontweight="bold", fontsize=14)

            # formatting
            all_axes[i][j].spines.right.set_visible(False)
            all_axes[i][j].spines.top.set_visible(False)
            all_axes[i][j].spines.bottom.set_visible(False)
            # add label to first y-axis
            if j == 0:
                all_axes[i][j].set_yticks(y_pos, labels=players, fontsize=12)
            else:
                all_axes[i][j].set_yticks([])
            # add label to bottom x-axis
            all_axes[i][j].set_xticks([])
            # add title to top bar
            if i == 0:
                all_axes[i][j].set_title(header_cols[j])

    # fig.suptitle(title,
    #             y=1.02, fontsize=28, fontweight="bold")
    fig_text(x=0.5, y=0.94, ha="center",
            fontsize=20, fontweight="bold",
            s="<Centre Back>  |  <Full Back>  |  <Midfielder>  |  <Attacker>",
            highlight_textprops=[{"color": '#4285F4'},
                                {"color": '#34A853'},
                                {"color": '#FBBC04'},
                                {"color": '#EA4335'}])
    plt.tight_layout()
    fig.subplots_adjust(top=0.88)

    # add banner
    add_banner(fig, title, team)

    return fig

def plot_bars(df, title, color):
    
    # load_fonts(font_path=font_path)
    # mpl.rcParams['font.family'] = 'Super Grotesk Pro'
    
    cols = df.columns
    x_ticks = df.index
    x = np.arange(len(x_ticks))
    
    fig, axes = plt.subplots(figsize=(14, 10), facecolor=(1, 1, 1),
                             nrows=len(cols), ncols=1)

    for i, ax in enumerate(axes):
        bars = ax.bar(x=df.index, height=df[cols[i]],
                      color=color, alpha=0.7, edgecolor="k",)

        # Add average line
        xmin, xmax = ax.get_xlim()
        team_avg = df[cols[i]].mean()
        ax.axhline(team_avg, ls="--", color="k", alpha=0.6, zorder=-2)
        ax.text(x=xmin, y=team_avg, s=f"Average\n{round(team_avg, 1)}",
                va="bottom", fontweight="bold", fontsize=12)
        
        # Formatting
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.spines.left.set_visible(False)
        
        # Title and Labels
        ax.set_title(cols[i], fontsize=16, fontweight="bold")
        if i == len(cols)-1:
            if len(x_ticks) > 3 :
                ax.set_xticks(x, labels=x_ticks, rotation=45, ha="right")
            else:
                ax.set_xticks(x, labels=x_ticks)
        else:
            ax.set_xticks([])
        ax.set_yticks([])
        
        bar_labels = [round(bar, 1) if bar != 0 else "" for bar in bars.datavalues]
        for j, val in enumerate(df[cols[i]]):
            if val == 0:
                continue
            if val >= team_avg:
                ax.text(x=j, y=val/2, s=round(val, 1), fontweight="bold",
                        ha="center", va="center", fontsize=12)
            else:
                ax.text(x=j, y=val, s=round(val, 1), fontweight="bold",
                        ha="center", va="bottom", fontsize=12)
    
    # title
    fig.suptitle(x=0.5, y=1, t=title, fontsize=26, fontweight="bold")
    fig.subplots_adjust(hspace=1)

    # add_banner(fig, title, None)

    return fig
