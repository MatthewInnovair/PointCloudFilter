# Python Script to filter points in a point cloud containing unwanted noise from water and clouds
# Looks for points with high brightness or blue levels 
import numpy as np
import pandas as pd

# Define the filter object
class Filter():
    '''
    Object containing filter parameters
    '''
    def __init__(self, blue_bool=True, blue_value=100, bright_bool=True, bright_value=145):
        '''
        Initialise filter object
        '''
        self.blue_bool = blue_bool               # switch blue filter on or off
        self.blue_value = blue_value             # blue filter value
        self.bright_bool = bright_bool           # switch brightness filter on or off
        self.bright_value = bright_value         # brightness filter value

    def blue(self, df):
        '''
        Pass pandas dataframe to filter, remove if Blue element is above filter value, return updated dataframe
        '''
        return df.drop(df[df.B > self.blue_value].index)
        
    def bright(self, df):
        '''
        Pass pandas dataframe to filter, remove if average of RGB values is above filter value, return updated dataframe
        '''
        df['brightness'] = df.apply(lambda row: self.get_brightness(row), axis=1)  # create brightness column
        return df.drop(df[df.brightness > self.bright_value].index)

    def all(self, df):
        '''
        Combine all filters, return completely filtered point cloud
        '''
        if self.bright_bool:
            df = self.bright(df)
        if self.blue_bool:
            df = self.blue(df)
        return df

    # Utility functions
    def get_brightness(self, row):
        '''
        Pass a pandas dataframe row
        Function returns brightness value as a mean of the RGB values
        '''
        return np.mean([row['R'],row['G'],row['B']])

### ******************** MAIN SCRIPT ******************** ###
# TODO: Put into Jupyter noteboook so steps can be separated

filter_point_cloud = Filter(blue_bool=True, blue_value=100, bright_bool=False, bright_value=145)  # establish the filter in the local workspace
names=['X','Y','Z','R','G','B']                                 # header names for point clouds
point_cloud = pd.read_csv('test.csv',header=None, names=names)  # create Pandas dataframe
point_cloud_filtered = filter_point_cloud.all(point_cloud)      # apply filter to point cloud
point_cloud_filtered.to_csv('filtered.csv', sep='\t', encoding='ascii') # save filtered point cloud to csv