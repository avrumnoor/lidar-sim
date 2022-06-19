import ipywidgets as widgets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from comparison_plot import plot_range
import pandas as pd
from ego import Ego
from lidar import Lidar
from parametric_study import (positive_horizontal_fov_slider, negative_horizontal_fov_slider,
                              resolution, sweep, excel_input)

from range_study import  (small_object_y_slider, small_object_z_slider, ped_min_points,
                          bike_min_points, car_min_points, truck_min_points, small_object_min_points,
                          y_axis_scale)


object_size_dict = {
    "Pedestrian": (100/1000, 440/1000),
    "Motorcycle": (660/1000, 660/1000),
    "Car": (1535/1000, 1282/1000),
    "Truck": (1560/1000, 1607/1000)
}

# df = pd.read_excel('lidar.xlsx')

# df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

# l1=Lidar("LR",(1.81, 1.841, 0), df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3), 0.4, 0, 0, 1)
# raydrop_range['value'] = False
e1=Ego(0, 0, 0, (3,1.8,2))

plot_output_sixth = widgets.Output()

def uploading_excel(excel_input, pos_hfov, neg_hfov, sweep):
    if len(excel_input) != 0: 
        uploaded_filename = list(excel_input.keys())[0]
        content = excel_input[uploaded_filename]['content']

        df = pd.read_excel(content)

        df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

        l=Lidar("LR",(1.81, 1.841, 0), 
                    df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3),
                    resolution, pos_hfov, neg_hfov, sweep=sweep)
        return l

def visulaize(ped_min_points, bike_min_points, car_min_points, truck_min_points,
              small_object_min_points, small_object_y_slider, small_object_z_slider,
              pos_hfov, neg_hfov, resolution1, resolution2, sweep1, sweep2, y_axis_scale, raydrop_range, excel_input1, excel_input2):

#     plot_output_sixth.clear_output()

    l1 = uploading_excel(excel_input1, pos_hfov, neg_hfov, sweep1)
    l2 = uploading_excel(excel_input2, pos_hfov, neg_hfov, sweep2)
    
#     with plot_output_sixth:
        
    l1.resolution = resolution1
    l2.resolution = resolution2

    plot_range(ped_min_points, bike_min_points, car_min_points, truck_min_points,
      small_object_min_points, small_object_y_slider, 
      small_object_z_slider, object_size_dict, e1, l1, l2, y_axis_scale, raydrop_range)
        
        




# apply_btn_comparison = widgets.Button(description='Compare Range Study')

raydrop_range = widgets.ToggleButton(description='Raydrop Mode')

excel_input1 = widgets.FileUpload(description='Lidar #1')

excel_input2 = widgets.FileUpload(description='Lidar #2')


def btn_eventhandler(obj):
    visulaize(ped_min_points.value, bike_min_points.value, car_min_points.value, truck_min_points.value,
     small_object_min_points.value, small_object_y_slider.value, small_object_z_slider.value,
     positive_horizontal_fov_slider.value, negative_horizontal_fov_slider.value,
     resolution.value, sweep.value, y_axis_scale.value, raydrop_range, excel_input1.value, excel_input2.value)
# apply_btn_comparison.on_click(btn_eventhandler)

