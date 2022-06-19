import ipywidgets as widgets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from range_plot import plot
import pandas as pd
from ego import Ego
from lidar import Lidar
from parametric_study import (positive_horizontal_fov_slider, negative_horizontal_fov_slider,
                              resolution, sweep, excel_input)


object_size_dict = {
    "Pedestrian": (100/1000, 440/1000),
    "Motorcycle": (660/1000, 660/1000),
    "Car": (1535/1000, 1282/1000),
    "Truck": (1560/1000, 1607/1000)
}

df = pd.read_excel('Velodyne_128_ingestion.xlsx')

df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

l1=Lidar("LR",(1.81, 1.841, 0), df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3), 0.4, 0, 0, 1)

e1=Ego(0, 0, 0, (3,1.8,2))

plot_output_fourth = widgets.Output()

def visulaize(ped_min_points, bike_min_points, car_min_points, truck_min_points,
              small_object_min_points, small_object_y_slider, small_object_z_slider,
              pos_hfov, neg_hfov, resolution, sweep, excel_input, y_axis_scale, raydrop_range):

    plot_output_fourth.clear_output()

    l1.pos_hfov = pos_hfov
    l1.neg_hfov = neg_hfov
    l1.sweep = sweep
    l_new = None
    if len(excel_input) != 0: 
        uploaded_filename = list(excel_input.keys())[0]
        content = excel_input[uploaded_filename]['content']

        df = pd.read_excel(content)

        df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

        l_new=Lidar("LR",(1.81, 1.841, 0), 
                    df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3),
                    resolution, pos_hfov, neg_hfov, sweep=sweep)

    with plot_output_fourth:
        if l_new == None:
            l1.resolution = resolution
            plot(ped_min_points, bike_min_points, car_min_points, truck_min_points,
              small_object_min_points, small_object_y_slider, 
              small_object_z_slider, object_size_dict, e1, l1, y_axis_scale, raydrop_range)
        else:
            l_new.resolution = resolution
            plot(ped_min_points, bike_min_points, car_min_points, truck_min_points,
              small_object_min_points, small_object_y_slider, 
              small_object_z_slider, object_size_dict, e1, l_new, y_axis_scale, raydrop_range)



small_object_y_slider = widgets.FloatSlider(min=0, max=5, description='small object y (m)',
                                            style= {'description_width': 'initial'}, value=0.4)
small_object_z_slider = widgets.FloatSlider(min=0, max=5, description='small object z (m)',
                                            style= {'description_width': 'initial'}, value=0.4)
ped_min_points = widgets.FloatText(description='Pedestrian min points', value=25,
                                   style= {'description_width': 'initial'})
bike_min_points = widgets.FloatText(description='Bike min points', value=30,
                                    style= {'description_width': 'initial'})
car_min_points = widgets.FloatText(description='Car min points', value=40,
                                   style= {'description_width': 'initial'})
truck_min_points = widgets.FloatText(description='Truck min points', value=40,
                                     style= {'description_width': 'initial'})
small_object_min_points = widgets.FloatText(description='Small object min points', value=60,
                                            style= {'description_width': 'initial'})
y_axis_scale = widgets.Dropdown(options=['linear', 'log'], description='Y axis scale')
apply_btn_range = widgets.Button(description='Run Range')

raydrop_range = widgets.ToggleButton(description='Raydrop Mode')


def btn_eventhandler(obj):
    visulaize(ped_min_points.value, bike_min_points.value, car_min_points.value, truck_min_points.value,
     small_object_min_points.value, small_object_y_slider.value, small_object_z_slider.value,
     positive_horizontal_fov_slider.value, negative_horizontal_fov_slider.value,
     resolution.value, sweep.value, excel_input.value, y_axis_scale.value, raydrop_range)
apply_btn_range.on_click(btn_eventhandler)
