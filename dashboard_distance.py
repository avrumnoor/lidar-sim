import ipywidgets as widgets
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from distance_to_stop_plot import plot_stop_distance


def calculate_distance(starting_speed, T_latency, T_BB, jerk, deceleration):

    plot_output.clear_output()
    starting_speed = 0.44704 * starting_speed
    
    V0_p3 = starting_speed - 0.5 * jerk * T_BB ** 2
    t_p3 = V0_p3 / deceleration
    
    X_AV_latency  = starting_speed * T_latency
    X_break_build = starting_speed * T_BB + jerk / 6 * (T_BB ** 3)
    X_constant    = V0_p3* t_p3 - 0.5 * deceleration *(t_p3 ** 2) 

    distance = X_AV_latency + X_break_build + X_constant

    with plot_output:
        plot_stop_distance(distance) 
    


plot_output = widgets.Output()

# starting_velocity = widgets.FloatText(description='starting_velocity (m/s)', 
#                         style= {'description_width': 'initial'}, value=20)
starting_speed = widgets.FloatSlider(min=0, max=60, description='starting speed (mph)',
                                     style= {'description_width': 'initial'},value=35)
T_latency = widgets.FloatText(description='t_latency (s)', 
                        style= {'description_width': 'initial'}, value=0.75)
T_BB = widgets.FloatText(description='t_bb (s)', 
                        style= {'description_width': 'initial'}, value=0.35)
jerk = widgets.FloatText(description='J (m/s^3)', 
                        style= {'description_width': 'initial'}, value=12)
# deceleration = widgets.FloatText(description='deceleration (m/s^2)', 
#                         style= {'description_width': 'initial'}, value=20)
deceleration = widgets.FloatSlider(min=0, max=10, description='dec (m/s^2)',
                                   style= {'description_width': 'initial'}, value=2)

apply_btn = widgets.Button(description='Run')





def btn_eventhandler(obj):
    calculate_distance(starting_speed.value, T_latency.value, T_BB.value, jerk.value, deceleration.value)


apply_btn.on_click(btn_eventhandler)

item_layout1 = widgets.Layout(margin='0 0 20px 0')
item_layout2 = widgets.Layout(margin='0 0 50px 0')


input_widgets1 = widgets.HBox([starting_speed, jerk, deceleration])
input_widgets2 = widgets.HBox([T_latency, T_BB,], layout=item_layout1)
input_widgets3 = widgets.HBox([apply_btn], layout=item_layout2)
# display(input_widgets)

tab = widgets.Tab([plot_output], layout=item_layout2)
tab.set_title(0, 'Distance to Stop')

# display(tab)

dashboard = widgets.VBox([input_widgets1, input_widgets2, input_widgets3, plot_output])
# display(dashboard)

