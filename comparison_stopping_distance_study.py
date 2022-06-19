import ipywidgets as widgets
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from comparison_distance_to_stop_plot import plot_stop_distance, plot_comparison_stop
from parametric_study import (target_y_slider, target_z_slider, excel_input,
                              positive_horizontal_fov_slider, negative_horizontal_fov_slider,
                              resolution, mountig_position_x, mountig_position_y,
                              mountig_position_z, sweep)
from range_study import  (small_object_y_slider, small_object_z_slider, ped_min_points,
                          bike_min_points, car_min_points, truck_min_points, small_object_min_points,
                          y_axis_scale)


from stopping_distance_study import (starting_speed, T_latency, T_BB, jerk, deceleration, apply_btn_distance,
                                     raydrop_distance)

from comparison_study import (excel_input1, excel_input2, small_object_y_slider, small_object_z_slider, y_axis_scale, ped_min_points, bike_min_points, car_min_points, truck_min_points, small_object_min_points, raydrop_range, plot_output_sixth)

from comparison_study import uploading_excel, visulaize

from ego import Ego
from lidar import Lidar
from target import Target
from pointcloud import PC

object_size_dict = {
    "Pedestrian": (100/1000, 440/1000),
    "Motorcycle": (660/1000, 660/1000),
    "Car": (1535/1000, 1282/1000),
    "Truck": (1560/1000, 1607/1000)
}


df = pd.read_excel('Velodyne_128_ingestion.xlsx')

df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

l1=Lidar("LR",(1.81, 1.841, 0), df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3), 0.4, 0, 0, sweep=1)

e1=Ego(0, 0, 0, (3,1.8,2))

def calculate_distance(T_latency, T_BB, jerk, deceleration,
                       target_y_slider, target_z_slider, excel_input1,
                       pos_hfov, neg_hfov, resolution, mountig_position_x,
                       mountig_position_y, mountig_position_z, sweep,
                       small_object_y_slider, small_object_z_slider,
                       ped_min_points, bike_min_points, car_min_points,
                       truck_min_points, small_object_min_points, y_axis_scale, raydrop_switch):

#     plot_output_sixth.clear_output()
    l1.pos_hfov = pos_hfov
    l1.neg_hfov = neg_hfov
    l1.sweep = sweep
    l_new = None
    if len(excel_input1) != 0: 
        uploaded_filename = list(excel_input1.keys())[0]
        content = excel_input1[uploaded_filename]['content']

        df = pd.read_excel(content)

        df.columns = ['channel', 'azimuth_offset', 'elevation_angle']

        l_new=Lidar("LR",(mountig_position_x, mountig_position_y, mountig_position_z), df['elevation_angle'].to_numpy(), df['azimuth_offset'].to_numpy(),(0.1,0.2,0.3), resolution, pos_hfov, neg_hfov, sweep=sweep)
    
        
    object_size_dict['SmallObj'] = (small_object_y_slider, small_object_z_slider)
    distance_points =[]
    for obj in object_size_dict:
        
        
        for starting_speed in range(81):
            
            starting_speed_ms = 0.44704 * starting_speed
        
            V0_p3 = starting_speed_ms - 0.5 * jerk * T_BB ** 2
            t_p3 = V0_p3 / deceleration

            X_AV_latency  = starting_speed_ms * T_latency
            X_break_build = starting_speed_ms * T_BB + jerk / 6 * (T_BB ** 3)
            X_constant    = V0_p3* t_p3 - 0.5 * deceleration *(t_p3 ** 2) 

            distance = X_AV_latency + X_break_build + X_constant


            t1 = Target((distance+ mountig_position_x ,0, 0), (4, object_size_dict[obj][0], object_size_dict[obj][1]))
        
        
            
            if l_new == None:
                l1.L_coordinate = (mountig_position_x, mountig_position_y, mountig_position_z)
                l1.resolution = resolution
                pc = PC(t1,e1,l1,0)
            else:
                l_new.L_coordinate = (mountig_position_x, mountig_position_y, mountig_position_z)
                l_new.resolution = resolution
                pc = PC(t1,e1,l_new,0)

            number_of_points = pc.get_filtered_points(object_size_dict[obj][0], object_size_dict[obj][1], mountig_position_z).shape[0] * pc.lidar.sweep

            distance_points.append([obj, starting_speed, distance, number_of_points])

        
    distance_points = np.array(distance_points)
#     distance_points = pd.DataFrame(distance_points)
#     distance_points.columns = ['object_type', 'speed', 'distance', 'number_of_points']
    return distance_points
    
    

    
    


plot_output_sixth = widgets.Output()

# # starting_velocity = widgets.FloatText(description='starting_velocity (m/s)', 
# #                         style= {'description_width': 'initial'}, value=20)
# starting_speed = widgets.FloatSlider(min=0, max=60, description='starting speed (mph)',
#                                      style= {'description_width': 'initial'},value=35)
# T_latency = widgets.FloatText(description='t_latency (s)', 
#                         style= {'description_width': 'initial'}, value=0.75)
# T_BB = widgets.FloatText(description='t_bb (s)', 
#                         style= {'description_width': 'initial'}, value=0.35)
# jerk = widgets.FloatText(description='J (m/s^3)', 
#                         style= {'description_width': 'initial'}, value=12)
# # deceleration = widgets.FloatText(description='deceleration (m/s^2)', 
# #                         style= {'description_width': 'initial'}, value=20)
# deceleration = widgets.FloatSlider(min=0, max=10, description='dec (m/s^2)',
#                                    style= {'description_width': 'initial'}, value=2)

resolution1 = widgets.FloatText(description='Lidar #1 Resolution', 
                         style= {'description_width': 'initial'}, value=0.4)

resolution2 = widgets.FloatText(description='Lidar #2 Resolution', 
                         style= {'description_width': 'initial'}, value=0.2)

sweep1 = widgets.FloatText(description='Lidar #1 Sweep', 
                         style= {'description_width': 'initial'}, value=1)

sweep2 = widgets.FloatText(description='Lidar #2 Sweep', 
                         style= {'description_width': 'initial'}, value=1)

apply_btn_comparison_stop = widgets.Button(description='Comparison',
                                    style= {'description_width': 'initial'})

# raydrop_distance = widgets.ToggleButton(description='Raydrop Mode')



def btn_eventhandler(obj):
    distance_points1 = calculate_distance(T_latency.value, T_BB.value, jerk.value, deceleration.value,
    target_y_slider.value, target_z_slider.value, excel_input1.value,
                              positive_horizontal_fov_slider.value, negative_horizontal_fov_slider.value,
                              resolution1.value, mountig_position_x.value, mountig_position_y.value,
                              mountig_position_z.value, sweep1.value,
                              small_object_y_slider.value, small_object_z_slider.value,
                              ped_min_points.value, bike_min_points.value, car_min_points.value, truck_min_points.value,
                              small_object_min_points.value, y_axis_scale.value, raydrop_distance)
    
    distance_points2 = calculate_distance(T_latency.value, T_BB.value, jerk.value, deceleration.value,
    target_y_slider.value, target_z_slider.value, excel_input2.value,
                              positive_horizontal_fov_slider.value, negative_horizontal_fov_slider.value,
                              resolution2.value, mountig_position_x.value, mountig_position_y.value,
                              mountig_position_z.value, sweep2.value,
                              small_object_y_slider.value, small_object_z_slider.value,
                              ped_min_points.value, bike_min_points.value, car_min_points.value, truck_min_points.value,
                              small_object_min_points.value, y_axis_scale.value, raydrop_distance)
    
    with plot_output_sixth:
        plot_output_sixth.clear_output()
        
        visulaize(ped_min_points.value, bike_min_points.value, car_min_points.value, truck_min_points.value,
     small_object_min_points.value, small_object_y_slider.value, small_object_z_slider.value,
     positive_horizontal_fov_slider.value, negative_horizontal_fov_slider.value,
     resolution1.value, resolution2.value, sweep1.value, sweep2.value, y_axis_scale.value, raydrop_range, excel_input1.value, excel_input2.value)
        
        
        plot_comparison_stop(distance_points1, distance_points2, ped_min_points.value, bike_min_points.value, car_min_points.value, truck_min_points.value,small_object_min_points.value, y_axis_scale.value, raydrop_distance) 
        
        


apply_btn_comparison_stop.on_click(btn_eventhandler)

# item_layout1 = widgets.Layout(margin='0 0 20px 0')
# item_layout2 = widgets.Layout(margin='0 0 50px 0')


# input_widgets1 = widgets.HBox([starting_speed, jerk, deceleration])
# input_widgets2 = widgets.HBox([T_latency, T_BB,], layout=item_layout1)
# input_widgets3 = widgets.HBox([apply_btn], layout=item_layout2)
# # display(input_widgets)

# tab = widgets.Tab([plot_output], layout=item_layout2)
# tab.set_title(0, 'Distance to Stop')

# # display(tab)

# dashboard = widgets.VBox([input_widgets1, input_widgets2, input_widgets3, plot_output])
# # display(dashboard)

