import pandas as pd
import numpy as np
from preprossec import path_df
from optimazation_functions import *
from visulaze import *

optimize_df = path_df.copy()

min_curv = float('inf')
for bias in range(2,3):
    for ratio in range(1, 7):
        ratio = ratio/10
        optimize_df = calculate_next_points(optimize_df, ratio, bias)
        curv_sum = calc_total_curvature(optimize_df, 'opt_p_x', 'opt_p_y')
        if curv_sum < min_curv:
            min_curv = curv_sum
        plot_points(optimize_df, 'x_left', 'y_left', 'x_right', 'y_right', 'opt_p_x', 'opt_p_y', ratio, bias, curv_sum)
print(min_curv)