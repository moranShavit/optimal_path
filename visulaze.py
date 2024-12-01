import preprossec
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from preprossec import path_df

def plot_points(df, x_left_col, y_left_col, x_right_col, y_right_col, x_center_col, y_center_col, ratio, bias, curv, avg_curv):
    """
    Plots left, right, and center points on a 2D plane with lines connecting the points for each category.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        x_left_col (str): Name of the column for left category X coordinates.
        y_left_col (str): Name of the column for left category Y coordinates.
        x_right_col (str): Name of the column for right category X coordinates.
        y_right_col (str): Name of the column for right category Y coordinates.
        x_center_col (str): Name of the column for center category X coordinates.
        y_center_col (str): Name of the column for center category Y coordinates.
    """
    plt.figure(figsize=(10, 8))

    # Color Mapping for categories
    colors = {'left': 'red', 'right': 'red', 'center': 'green'}

    # Categories
    categories = ['left', 'right', 'center']

    # Loop through each category and plot
    for cat in categories:
        # Dynamically get the column names based on category
        x_col = locals()[f'x_{cat}_col']
        y_col = locals()[f'y_{cat}_col']

        # Remove NaN values from x and y columns
        x = df[x_col].dropna()
        y = df[y_col].dropna()

        # Plot each category's points with small markers (s=1)
        plt.scatter(x, y, label=cat, color=colors[cat], marker='o', s=1)

        # Connect the points within the same category
        plt.plot(x, y, color=colors[cat], linestyle='--', alpha=0.7)

    # Add labels, title, and legend
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title(f'Parameters - ratio: {ratio} , bias : {bias}, curv_sum : {curv}, avg_curv : {avg_curv}')
    plt.legend(title='Category')

    # Show grid and plot
    plt.grid(True)
    plt.show()

