import pandas as pd
import numpy as np
from preprossec import path_df
from optimazation_functions import *
from visulaze import *


def check_path(df, ratio, bias, outer_border_x_col, outer_border_y_col, inner_border_x_col, inner_border_y_col ):
    """
    Checks and visualizes the calculated path by optimizing the points based on curvature and plotting the results.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the coordinates and other necessary data for the path.
    ratio : float
        A weight factor used in the `calculate_next_points` function to adjust the tangent's influence.
    bias : int
        The number of rows forward to consider when calculating the optimized path.
    outer_border_x_col : str
        The column name in the DataFrame for the X-coordinates of the outer border.
    outer_border_y_col : str
        The column name in the DataFrame for the Y-coordinates of the outer border.
    inner_border_x_col : str
        The column name in the DataFrame for the X-coordinates of the inner border.
    inner_border_y_col : str
        The column name in the DataFrame for the Y-coordinates of the inner border.

    Returns:
    -------
    None
        This function does not return any value. It plots the results and computes curvature statistics.

    Workflow:
    ---------
    1. **Copy Input DataFrame:** Creates a copy of the input DataFrame to avoid modifying the original.
    2. **Calculate Optimized Points:** Calls `calculate_next_points` to compute the optimized points for the path.
    3. **Compute Curvature:** Calls `calc_total_curvature` to calculate the total curvature and average curvature of the path.
    4. **Visualization:** Calls `plot_points` to visualize the optimized path alongside the inner and outer borders,
       and overlays curvature-related information.

    Notes:
    ------
    - The function assumes that the `calculate_next_points`, `calc_total_curvature`, and `plot_points` functions
      are already implemented and available.
    - Visualization provides insights into the path's smoothness and how well it adheres to the curvature constraints.
    """
    temp_df = df.copy()
    temp_df = calculate_next_points(temp_df, ratio, bias)
    curv_sum, avg_curv = calc_total_curvature(temp_df, "opt_p_x", "opt_p_y")
    plot_points(temp_df, inner_border_x_col, inner_border_y_col, outer_border_x_col, outer_border_y_col,
                "opt_p_x", "opt_p_y", ratio, bias, curv_sum, avg_curv)
def expirement(ratio_range_int, bias_range):
    """
    Finds the optimal ratio and bias values to minimize total and average curvature.

    Parameters:
    ----------
    ratio_range_int : int
        The upper limit for the ratio range (divided by 10 in the loop).
    bias_range : int
        The range of bias values to test.

    Returns:
    -------
    None
        Prints the minimal total curvature and corresponding average curvature, ratio, and bias values.

    Workflow:
    ---------
    1. Loops through all combinations of ratio (scaled by 10) and bias values.
    2. Calculates optimized points and corresponding curvature for each combination.
    3. Tracks and prints the configuration yielding the minimal total and average curvature.

    Notes:
    ------
    - Relies on global `path_df` for the initial data.
    - Calls `calculate_next_points` and `calc_total_curvature` for point generation and curvature calculation.
    """
    min_total_curv = float('inf')
    min_avg_curv = float('inf')
    min_total_data = [0,0,0]
    min_avg_curv_data = [0,0,0]
    for bias in range(0,bias_range):
        for ratio in range(1, ratio_range_int):
            optimize_df = path_df.copy()
            ratio = ratio/10
            optimize_df = calculate_next_points(optimize_df, ratio, bias)
            curv_sum, avg_curv = calc_total_curvature(optimize_df, 'opt_p_x', 'opt_p_y')
            if curv_sum < min_total_curv:
                min_total_curv = curv_sum
                min_total_data[0] = ratio
                min_total_data[1] = bias
                min_total_data[2] = avg_curv
            if avg_curv < min_avg_curv:
                min_avg_curv = avg_curv
                min_avg_curv_data[0] = ratio
                min_avg_curv_data[1] = bias
                min_avg_curv_data[2] = min_total_curv

    print("min_total_curv: ", min_total_curv , "avg_curv: ", min_total_data[2], "ratio: ", min_total_data[0], "bias: ", min_total_data[1])
    print( "min_avg_curv: ", "total_curv: ", min_avg_curv_data[2], min_avg_curv , "ratio: ", min_avg_curv_data[0], ", bias: ", min_avg_curv_data[1])


