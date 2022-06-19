import pandas as pd
from ego import Ego
from lidar import Lidar
from target import Target
from pointcloud import PC
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets


# object_size_dict = {
#     "None": (0, 0),
#     "Pedestrian": (440, 100),
#     "Motorcycle": (660, 660),
#     "Car": (1282, 1535),
#     "Truck": (1607,1560)
# }

# object_size_dict = {
#     "None": (0, 0),
#     "Pedestrian": (100, 440),
#     "Motorcycle": (660, 660),
#     "Car": (1535, 1282),
#     "Truck": (1560,1607)
# }

object_size_dict = {
    "None": (0, 0),
    "Pedestrian": (720, 1750),
    "Motorcycle": (1580, 1460),
    "Car": (1880, 1780),
    "Truck": (2450,3000)
}

df = pd.read_excel('Velodyne_128_ingestion.xlsx')

df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

l1=Lidar("LR",(1.81, 1.841, 0), df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3), 0.4, 0, 0, sweep=1)

e1=Ego(0, 0, 0, (3,1.8,2))

plot_output_first = widgets.Output()
plot_output_second = widgets.Output()
plot_output_third = widgets.Output()

resolution = widgets.FloatText(description='resolution', value=0.4)
mountig_position_z = widgets.BoundedFloatText(description='mountig_position_z (m)', 
                        style= {'description_width': 'initial'}, value=0, min=-2, max=2)
mountig_position_y = widgets.BoundedFloatText(description='mountig_position_y (m)', 
                        style= {'description_width': 'initial'}, value=1.841, min=0.5, max=4)
mountig_position_x = widgets.BoundedFloatText(description='mountig_position_x (m)', 
                        style= {'description_width': 'initial'}, value=1.81, min=0, max=10)
target_y_slider = widgets.FloatSlider(min=0, max=10, description='target_y (m)')
target_z_slider = widgets.FloatSlider(min=0, max=20, description='target_z (m)')
distance = widgets.FloatSlider(min=0, max=50, description='distance (m)', value=25)
excel_input = widgets.FileUpload(description='excel_input')
object_type = widgets.Dropdown(options=['None', 'Pedestrian', 'Motorcycle', 'Car', 'Truck'], description='Target Type')
positive_horizontal_fov_slider = widgets.FloatSlider(min=0, max=180, description='pos_hfov (degree)', 
                                                     style= {'description_width': 'initial'}, value=3)
negative_horizontal_fov_slider = widgets.FloatSlider(min=0, max=180, description='neg_hfov (degree)', 
                                                     style= {'description_width': 'initial'}, value=3)
sweep = widgets.Dropdown(options=list(range(1,11)), description='Sweep')
apply_btn_parametric = widgets.Button(description='Run Parametric')

raydrop_switch = widgets.ToggleButton(description='Raydrop Mode')
    
    
def plot_params(distance, target_y_slider, target_z_slider, excel_input,
                pos_hfov, neg_hfov, resolution, mountig_position_z,
                mountig_position_y, mountig_position_x, sweep, raydrop_switch):
    
    plot_output_first.clear_output()
    plot_output_second.clear_output()
    plot_output_third.clear_output()
    
    l1.pos_hfov = pos_hfov
    l1.neg_hfov = neg_hfov
    l1.sweep = sweep
    l_new = None
    if len(excel_input) != 0: 
        uploaded_filename = list(excel_input.keys())[0]
        content = excel_input[uploaded_filename]['content']

        df = pd.read_excel(content)

        df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

        l_new=Lidar("LR",(mountig_position_x, mountig_position_y, mountig_position_z), df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3), resolution, pos_hfov, neg_hfov, sweep=sweep)
    
    
    t1 = Target((distance+ mountig_position_x ,0, 0), (4, target_y_slider, target_z_slider))
    
        
    if l_new == None:
        l1.L_coordinate = (mountig_position_x, mountig_position_y, mountig_position_z)
        l1.resolution = resolution
        pc = PC(t1,e1,l1, raydrop_switch)
    else:
        l_new.L_coordinate = (mountig_position_x, mountig_position_y, mountig_position_z)
        l_new.resolution = resolution
        pc = PC(t1,e1,l_new, raydrop_switch)
    
#     print(mountig_position_x, mountig_position_y, mountig_position_z, target_y_slider, target_z_slider,)
    
    with plot_output_first:
        pc.visuals_first(target_y_slider, target_z_slider, mountig_position_z, object_type)
        
        
#     ## For simulating range of distances
#     for dist in range(1,101):
#         t1 = Target((dist+ mountig_position_x ,0, 0), (4, target_y_slider, target_z_slider))
#         l1.L_coordinate = (mountig_position_x, mountig_position_y, mountig_position_z)
#         l1.resolution = resolution
#         pc = PC(t1,e1,l1, raydrop_switch)
#         pc.visuals_first(target_y_slider, target_z_slider, mountig_position_z, object_type)
        
        
    with plot_output_second:
        pc.visuals_second(target_y_slider, target_z_slider, mountig_position_z, object_type)
    
    with plot_output_third:
        pc.visuals_third(target_y_slider, target_z_slider, mountig_position_z, object_type)
        
    
def object_type_eventhandler(change):
    target_y_slider.value = object_size_dict[change.new][0] / 1000
    target_z_slider.value = object_size_dict[change.new][1] / 1000
    
    

def mountig_position_x_handler(change):
    
    distance.value = distance.value + change.old - change.new


object_type.observe(object_type_eventhandler, names='value')
mountig_position_x.observe(mountig_position_x_handler, names='value')



def btn_eventhandler(obj):
    plot_params(distance.value, target_y_slider.value, target_z_slider.value, excel_input.value,
                positive_horizontal_fov_slider.value, negative_horizontal_fov_slider.value, resolution.value, mountig_position_z.value,
                mountig_position_y.value, mountig_position_x.value, sweep.value, raydrop_switch)
apply_btn_parametric.on_click(btn_eventhandler)


