import ipywidgets as widgets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from range_plot import plot
import pandas as pd
from ego import Ego
from lidar import Lidar
import json
# from parametric_study import (positive_horizontal_fov_slider, negative_horizontal_fov_slider,
#                               resolution, sweep, excel_input)


# object_size_dict = {
#     "Pedestrian": (100/1000, 440/1000),
#     "Motorcycle": (660/1000, 660/1000),
#     "Car": (1535/1000, 1282/1000),
#     "Truck": (1560/1000, 1607/1000)
# }

obj_names = {'ped' : 'Pedestrian',
              'bike' : 'Bike',
              'short_vehicle' : 'Car',
              'long_vehicle' : 'Truck',
             'trafficcone' : 'Traffic Cones',
              'genericobjects' : 'Generic Objects',
             'czone_signs' : 'CZone Signs'
        }

plot_output_seventh = widgets.Output()

def interpolation_estimator(n_test, data):
    
    if n_test < data['n_points'][0]:
        return data['means'][0], data['stds'][0]
    
    if n_test > data['n_points'][-1]:
        return data['means'][-1], data['stds'][-1]
    
    ind = 1
    
    while ind < len(data['means']):
        
        if data['n_points'][ind] >= n_test >= data['n_points'][ind-1]:
            
#             ind = len(data['n_points']) + 1
            break
        
        ind += 1
        
    upper = data['n_points'][ind]
    lower = data['n_points'][ind-1]
    
    ratio = (n_test - lower) / (upper-lower)
    increment_mean = (data['means'][ind] - data['means'][ind-1]) * ratio
    res_mean = data['means'][ind-1] + increment_mean
    
    increment_std = (data['stds'][ind] - data['stds'][ind-1]) * ratio
    res_std = data['stds'][ind-1] + increment_std
    
    return res_mean, res_std

def visulaize(F1_ped_min_points, F1_bike_min_points, F1_car_min_points, F1_truck_min_points,F1_traffic_cone_min_points,
              F1_small_object_min_points, F1_czone_signs_min_points):


        plot_output_seventh.clear_output()
        
        f = open('../F1 Score Means and Standard Deviations/F1_means_stds.json')
        raw_data = json.load(f)
        f.close()
        
        thresholds = {'ped' : F1_ped_min_points,
                      'bike' : F1_bike_min_points,
                      'short_vehicle' : F1_car_min_points,
                      'long_vehicle' : F1_truck_min_points,
                      'trafficcone' : F1_traffic_cone_min_points,
                      'genericobjects' : F1_small_object_min_points,
                      'czone_signs': F1_czone_signs_min_points
        }
        
        with plot_output_seventh:
                       
            print('Attention: These results are based on data collected from VLS-128 and LSN Gen2 \n' )   
             
            for key in thresholds:
                
                data = raw_data[key]
                
                pred_mean, pred_std = interpolation_estimator(thresholds[key],data)

                out_str = "{0:<13}{1:<15}{2:<13}{3:<5}{4:<15}{5:<5} \n".format('F1 Score for ', obj_names[key],  
                '  ->   Mean:',str(format(pred_mean, ".2f")), '   Std. Dev: ', str(format(pred_std, ".2f")))
                
                print(out_str)



F1_ped_min_points = widgets.FloatText(description='Pedestrian min points', value=78,
                                   style= {'description_width': 'initial'})
F1_bike_min_points = widgets.FloatText(description='Bike min points', value=87,
                                    style= {'description_width': 'initial'})
F1_car_min_points = widgets.FloatText(description='Car min points', value=62,
                                   style= {'description_width': 'initial'})
F1_truck_min_points = widgets.FloatText(description='Truck min points', value=3000,
                                     style= {'description_width': 'initial'})
F1_traffic_cone_min_points = widgets.FloatText(description='Traffic Cone min points', value=64,
                                            style= {'description_width': 'initial'})
F1_small_object_min_points = widgets.FloatText(description='Generic Objects min points', value=400,
                                            style= {'description_width': 'initial'})
F1_czone_signs_min_points = widgets.FloatText(description='CZone Signs min points', value=760,
                                            style= {'description_width': 'initial'})

apply_btn_F1_score = widgets.Button(description='Estimate F1 Score')


def btn_eventhandler(obj):
    visulaize(F1_ped_min_points.value, F1_bike_min_points.value, F1_car_min_points.value, F1_truck_min_points.value,
     F1_traffic_cone_min_points.value, F1_small_object_min_points.value, F1_czone_signs_min_points.value)
apply_btn_F1_score.on_click(btn_eventhandler)
