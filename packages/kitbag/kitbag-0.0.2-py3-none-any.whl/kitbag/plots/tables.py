import re
import os
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
from highlight_text import fig_text

from ..utils.colors import grey, red, green, blue, yellow
from ..utils.utilities import add_banner, shift_row_to_bottom


def plot_table(df, title, main_col=None):
    
    # load_fonts(font_path=font_path)
    # mpl.rcParams['font.family'] = 'Super Grotesk Pro'
    
    if main_col:
        df_plot = df.sort_values(main_col)
    else:
        df_plot = df.sort_values("Date", ascending=False)
    
    if "Average" in list(df_plot.iloc[:, 0]):
        # get index of average column
        average_idx = df_plot.index[df_plot.iloc[:, 0]=="Average"].tolist()
        df_plot = shift_row_to_bottom(df_plot, average_idx[0])
    
    # setup viz
    fig, ax = plt.subplots(figsize=(20, 12))

    # set rows and columns
    rows, cols = df_plot.index, df_plot.columns
    nrows, ncols = len(rows), len(cols)
    header_cols = [col.replace("(", "\n"+"(", 1) for col in cols]
    header_cols = [col.replace(" per", "\n"+"per", 1) for col in header_cols]
    
    # add padding
    xmin, xmax = ax.set_xlim(0, ncols + 0.5)
    ymin, ymax = ax.set_ylim(-1, nrows + 1)
    
    for i, player in enumerate(df_plot.iloc[:, 0]):
        # extract the row data from the list
        d = df_plot[df_plot.iloc[:, 0] == player]
        
        # the y (row) coordinate is based on the row index (loop)
        for j, col in enumerate(cols):
            # the x (column) coordinate is defined based on the order I want to display the data in
            # player name column
            if col == main_col:
                ax.text(x=j, y=i, s=d[col].values[0], fontsize=16, va='center', ha='left', fontweight="bold")
                # add highlight to main col
                rect = patches.Rectangle(
                    (j-0.1, -0.4),  # bottom left starting position (x,y)
                    .6, ymax*0.95,  # width and height
                    ec='none', fc='grey', alpha=.02, zorder=-1)
                ax.add_patch(rect)
            # make name text small
            elif col == cols[0]:
                txt = ax.text(x=j+0.5, y=i, s=d[col].values[0], fontsize=16, va='center', ha='right')
            else:
                txt = ax.text(x=j, y=i, s=d[col].values[0], fontsize=16, va='center', ha='left')
            
            # set background color of biggest number
            try:
                if float(txt.get_text()) == df_plot[col].max():
                    txt.set_backgroundcolor(green+"99")
            except (ValueError, TypeError):
                txt.set_backgroundcolor("w")
            
            # add column header
            if col == cols[0]:
                ax.text(x=j+0.5, y=ymax*0.96, s=header_cols[j], fontsize=14, fontweight="bold", ha="right")
            else:
                ax.text(x=j, y=ymax*0.96, s=header_cols[j], fontsize=14, fontweight="bold", ha="left")

    # add row divider
    for row in range(nrows):
        ax.plot([0, ncols], [row -.5, row - .5],
                ls=':', lw='.5', c='k', alpha=0.6)
    # add header divider
    ax.plot([0, ncols], [ymax*0.95, ymax*0.95],
            lw='.75', c='black')
    
    # remove spines, ticks etc.
    ax.axis('off')
    
    # add global title
    fig.suptitle(title, fontsize=26, fontweight="bold")


    return fig
