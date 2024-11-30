import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Read the CSV file containing track data
df = pd.read_csv('C:\\Users\\moran\\personal_projects\\optimal_curvature\\BrandsHatchLayout.csv')

# Filter the data to separate points on the left and right sides of the track
# 'side' column is expected to have values like 'left' or 'right'
left_df = df[df['side'] == 'left']
right_df = df[df['side'] == 'right']

# Reset the index for both DataFrames to ensure sequential indexing
right_df = right_df.reset_index(drop=True)
left_df = left_df.reset_index(drop=True)

# Merge the left and right DataFrames on their indices
# This aligns corresponding left and right side points
path_df = pd.merge(left_df, right_df, left_index=True, right_index=True, how='inner')
path_df = path_df.rename(columns={
    'x_x': 'x_left',
    'y_x': 'y_left',
    'x_y': 'x_right',
    'y_y': 'y_right'
})
path_df = path_df.drop(['side_x', 'side_y'], axis=1)

# Calculate the centerline points of the track
# The centerline is the average of the left and right side coordinates
path_df['x_center'] = (path_df['x_left'] + path_df['x_right'])/2
path_df['y_center'] = (path_df['y_left'] + path_df['y_right'])/2
path_df = path_df.dropna()



