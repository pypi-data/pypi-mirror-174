import re
import os
import numpy as np
import streamlit as st

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from highlight_text import fig_text

import altair as alt
from PIL import Image

blue = "#4285F4"
green = "#34A853"
yellow = "#FBBC04"
red = "#EA4335"


def plot_altair_scatter(df, x, y, title, tooltip, width, height, color, size, label=None):
    
    selection_val = re.sub(":.*$", "", color)
    selection = alt.selection_multi(fields=[selection_val], bind="legend")
    
    scatter = alt.Chart(df).mark_circle(size=size).encode(
        x=alt.X(x),
        y=alt.Y(y),
        tooltip=tooltip,
        color=alt.Color(color,
                        legend=alt.Legend()),
        opacity=alt.condition(selection, alt.value(1), alt.value(0))
    ).properties(
        title=title,
        width=width,
        height=height,
    )
    
    if label:
        text = scatter.mark_text(
            align="left",
            baseline="middle"
        ).encode(
            color=alt.value("black"),
            text=label
        )
        return (scatter + text).interactive().add_selection(selection)
    else:
        return scatter.interactive().add_selection(selection)