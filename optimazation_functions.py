import pandas as pd
import numpy as np
from preprossec import path_df
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def incline_calc(cur_p_x, cur_p_y, last_p_x, last_p_y, next_center_p_x, next_center_p_y, ratio):
    """
    Calculates a weighted slope combining the tangent and centerline slopes.

    Parameters:
    ----------
    cur_p_x : float
        The x-coordinate of the current point.
    cur_p_y : float
        The y-coordinate of the current point.
    last_p_x : float
        The x-coordinate of the previous point.
    last_p_y : float
        The y-coordinate of the previous point.
    next_center_p_x : float
        The x-coordinate of the center point for the next segment.
    next_center_p_y : float
        The y-coordinate of the center point for the next segment.
    ratio : float
        A weighting factor for combining the tangent slope and the centerline slope.
        - `1.0`: Full weight to the tangent slope.
        - `0.0`: Full weight to the centerline slope.

    Returns:
    -------
    float
        The weighted slope based on the ratio.
    """
    tangent = ((cur_p_y - last_p_y)/(cur_p_x - last_p_x))
    center_incline = (next_center_p_y - cur_p_y)/(next_center_p_x - cur_p_x)
    return ((tangent*ratio) + center_incline*(1-ratio))


def find_intersection(m1, b1, m2, b2):
    """
    Finds the intersection point of two lines defined by their slopes and intercepts.

    Parameters:
    ----------
    m1 : float
        Slope of the first line.
    b1 : float
        Intercept of the first line.
    m2 : float
        Slope of the second line.
    b2 : float
        Intercept of the second line.

    Returns:
    -------
    tuple
        A tuple `(x, y)` representing the coordinates of the intersection point.

    Raises:
    ------
    LinAlgError
        If the lines are parallel (no intersection) or the coefficients form a singular matrix.
    """
    # Create the coefficient matrix and the constant vector
    A = np.array([[m1, -1], [m2, -1]])
    B = np.array([-b1, -b2])

    # Solve the system of equations
    x, y = np.linalg.solve(A, B)

    return x, y

def calc_next_point(cur_p_x, cur_p_y, n_outer_border_p_x, n_outer_border_p_y, n_inner_border_p_x, n_inner_border_p_y,incline):
    """
    Calculates the next point along a path given the current point, next border points, and an incline.

    Parameters:
    ----------
    cur_p_x : float
        X-coordinate of the current point.
    cur_p_y : float
        Y-coordinate of the current point.
    n_outer_border_p_x : float
        X-coordinate of the next outer border point.
    n_outer_border_p_y : float
        Y-coordinate of the next outer border point.
    n_inner_border_p_x : float
        X-coordinate of the next inner border point.
    n_inner_border_p_y : float
        Y-coordinate of the next inner border point.
    incline : float
        Slope of the tangent line at the current point.

    Returns:
    -------
    tuple
        A tuple `(x, y)` representing the coordinates of the next point.

    Notes:
    ------
    - The function calculates the intersection of two lines:
        - A tangent line passing through the current point.
        - A line passing through the next inner and outer border points.
    - If the intersection lies within the boundary defined by the next border points, it is returned.
    - If the intersection is outside the boundary, a point is selected based on proximity to the borders.
    - Adjustments to the point are made based on whether it is closer to the inner or outer border.

    """
    next_line_inc = (n_outer_border_p_y - n_inner_border_p_y)/(n_outer_border_p_x - n_inner_border_p_x)
    b_next = n_inner_border_p_y - (next_line_inc * n_inner_border_p_x)
    b_tan = cur_p_y - (incline*cur_p_x)

    x,y = find_intersection(incline, b_tan, next_line_inc, b_next)
    # Find the minimum and maximum coordinates for both x and y
    x_min = min(n_inner_border_p_x, n_outer_border_p_x)
    x_max = max(n_inner_border_p_x, n_outer_border_p_x)
    y_min = min(n_inner_border_p_y, n_outer_border_p_y)
    y_max = max(n_inner_border_p_y, n_outer_border_p_y)

    # Check if the point (x, y) is inside the square
    if  x_min <= x <= x_max and y_min <= y <= y_max:
        return x, y
    else:
        if distance(x,y,n_outer_border_p_x, n_outer_border_p_y) < distance(x,y,n_inner_border_p_x, n_inner_border_p_y):
            x = n_outer_border_p_x*0.8 + n_inner_border_p_x*0.2
            y = n_outer_border_p_y*0.8 + n_inner_border_p_y*0.2
        else:
            x = n_inner_border_p_x*0.8 + n_outer_border_p_x*0.2
            y = n_inner_border_p_y*0.8 + n_outer_border_p_y*0.2
    return x,y



def calc_curvature(cur_p_x, cur_p_y, n_p_x, n_p_y, last_p_x, last_p_y):
        """
        Calculates the curvature at a given point based on the tangent of the line between points and the slope
        of a line between the current point and the next point along the path.

        Parameters:
        ----------
        cur_p_x : float
            X-coordinate of the current point.
        cur_p_y : float
            Y-coordinate of the current point.
        n_p_x : float
            X-coordinate of the next point along the path.
        n_p_y : float
            Y-coordinate of the next point along the path.
        last_p_x : float
            X-coordinate of the previous point along the path.
        last_p_y : float
            Y-coordinate of the previous point along the path.

        Returns:
        -------
        float
            The absolute difference in the angles (in degrees) between the tangent of the line from the previous point
            to the current point, and the slope of the line between the current point and the next point. This represents
            the curvature of the path at the current point.

        Notes:
        ------
        - **Tangent Calculation:** The tangent is calculated as the slope between the previous point and the current point.
        - **Slope Between Points:** The slope between the current point and the next point is also calculated.
        - **Angle Difference:** The function returns the absolute difference between the angles of the two lines, which gives the curvature.
        """
        next_inc = ((n_p_y - cur_p_y)/(n_p_x - cur_p_x ))
        tangent = (cur_p_y - last_p_y) / (cur_p_x - last_p_x)
        angle_radians_n_inc = math.atan(next_inc)
        angle_radians_tangent = math.atan(tangent)

        # Convert the angle to degrees
        angle_degrees_next_inc = math.degrees(angle_radians_n_inc)
        angle_degrees_tangent = math.degrees(angle_radians_tangent)

        return abs(angle_degrees_tangent - angle_degrees_next_inc)


def calc_total_curvature(df, x_column, y_column):
    """
    Calculates the total curvature along a path by summing the curvatures between successive points.

    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame containing the coordinates of the path and inner border points.
    x_column : str
        Name of the column in `df` for the X-coordinates of the path points.
    y_column : str
        Name of the column in `df` for the Y-coordinates of the path points.
    inner_x_column : str
        Name of the column in `df` for the X-coordinates of the inner border points.
    inner_y_column : str
        Name of the column in `df` for the Y-coordinates of the inner border points.

    Returns:
    -------
    float
        The total curvature along the path, summed across all points where the curvature is positive.

    Notes:
    ------
    - **Curvature Calculation:** Uses the `calc_curvature` function to compute the curvature at each point along the path.

    Raises:
    ------
    IndexError
        If the DataFrame does not have sufficient rows to compute curvatures (fewer than two points).
    """
    total_curvature = 0
    count = 0
    for i in range(2,len(df)-1):
        curv = abs((calc_curvature(df[x_column][i], df[y_column][i], df[x_column][i+1],
                                          df[x_column][i+1], df[x_column][i-1], df[y_column][i-1])))
        if curv > 0:
            total_curvature += curv
            count += 1
    avg_curvature = total_curvature/count
    return total_curvature, avg_curvature




def calculate_next_points(df, ratio, row_forward):
    """
    Calculates the next optimal points (`opt_p_x`, `opt_p_y`) along a path by iterating through
    the DataFrame and using the `calc_next_point` function.

    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame containing the path and center coordinates.
    ratio : float
        The ratio that influences the combination of tangent and center incline in the curvature calculation.
    row_forward : int
        The number of rows to look ahead when calculating the next point (how far ahead the "next few rows" should be).

    Returns:
    -------
    pandas.DataFrame
        The updated DataFrame with calculated `opt_p_x` and `opt_p_y` columns.

    Notes:
    ------
    - **Initial Points:** The first few rows are initialized with the center points as their respective `opt_p_x` and `opt_p_y` values.
    - **Curvature Calculation:** The `incline_calc` function is used to determine the incline, which is passed to `calc_next_point`.
    - **Forward Calculation:** The calculation considers the row specified by `row_forward` for the next few rows.

    Raises:
    ------
    IndexError
        If there are not enough rows to perform calculations when `row_forward` is used.
    """
    # Initialize the next point columns
    df['opt_p_x'] = np.nan
    df['opt_p_y'] = np.nan

    # Initialize the first row's next point to the center point of the first row
    df.at[1, 'opt_p_x'] = df.at[1, 'x_center']
    df.at[1, 'opt_p_y'] = df.at[1, 'y_center']
    df.at[2, 'opt_p_x'] = df.at[2, 'x_center']
    df.at[2, 'opt_p_y'] = df.at[2, 'y_center']

    # Start calculating from the second row (index 2, which corresponds to row 2 of the data)
    for i in range(2, len(df)-row_forward):
        last_row = df.iloc[i-2]
        cur_row = df.iloc[i - 1]
        next_row = df.iloc[i]
        next_few_row = df.iloc[i+row_forward]
        # Call the calc_next_point function using the current and previous row values
        next_p_x, next_p_y = calc_next_point(
            cur_row['opt_p_x'],
            cur_row['opt_p_y'],
            next_row['x_left'],
            next_row['y_left'],
            next_row['x_right'],
            next_row['y_right'],
            incline_calc(cur_row['opt_p_x'], cur_row['opt_p_y'], last_row['opt_p_x'], last_row['opt_p_y'],
                         next_few_row['x_center'], next_few_row['y_center'], ratio)
        )

        # Store the result in the next_p_x and next_p_y columns
        df.loc[i+1, 'opt_p_x'] = next_p_x
        df.loc[i+1, 'opt_p_y'] = next_p_y

    return df
