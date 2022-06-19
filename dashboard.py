import ipywidgets as widgets
from parametric_study import (mountig_position_x, mountig_position_y, mountig_position_z, excel_input,
                              object_type, resolution, positive_horizontal_fov_slider, negative_horizontal_fov_slider,
                              distance, sweep, target_y_slider, target_z_slider, apply_btn_parametric, plot_output_first,
                              plot_output_second, plot_output_third, raydrop_switch)
from range_study import (small_object_y_slider, small_object_z_slider, y_axis_scale, ped_min_points,
                         bike_min_points, car_min_points, truck_min_points, small_object_min_points,
                         apply_btn_range, plot_output_fourth, raydrop_range)
from stopping_distance_study import (starting_speed, T_latency, T_BB, jerk, deceleration, apply_btn_distance,
                                     plot_output_fifth, raydrop_distance)

from comparison_study import (excel_input1, excel_input2, small_object_y_slider, small_object_z_slider, y_axis_scale, ped_min_points,
                         bike_min_points, car_min_points, truck_min_points, small_object_min_points,plot_output_sixth)

from comparison_stopping_distance_study import (apply_btn_comparison_stop, resolution1, resolution2, sweep1, sweep2, plot_output_sixth)

from F1_score_study import (F1_ped_min_points, F1_bike_min_points, F1_car_min_points, F1_truck_min_points,
              F1_traffic_cone_min_points, F1_small_object_min_points, F1_czone_signs_min_points, apply_btn_F1_score, plot_output_seventh)


item_layout1 = widgets.Layout(margin='0 0 20px 0')
item_layout2 = widgets.Layout(margin='0 0 50px 0')


input_widgets1 = widgets.HBox([mountig_position_z, mountig_position_y, mountig_position_x])
input_widgets2 = widgets.HBox([excel_input, object_type, resolution])
input_widgets3 = widgets.HBox([positive_horizontal_fov_slider, negative_horizontal_fov_slider, sweep])
input_widgets4 = widgets.HBox([distance, target_y_slider, target_z_slider], layout=item_layout1)
# input_widgets13 = widgets.HBox([raydrop_switch])
input_widgets5 = widgets.HBox([raydrop_switch, apply_btn_parametric], layout=item_layout2)

input_widgets17 = widgets.HBox([F1_ped_min_points, F1_bike_min_points, F1_car_min_points])
input_widgets18 = widgets.HBox([F1_truck_min_points, F1_traffic_cone_min_points, F1_small_object_min_points])
input_widgets19 = widgets.HBox([F1_czone_signs_min_points, apply_btn_F1_score], layout=item_layout2)

input_widgets6 = widgets.HBox([small_object_y_slider, small_object_z_slider, y_axis_scale])
input_widgets7 = widgets.HBox([ped_min_points, bike_min_points, car_min_points])
input_widgets8 = widgets.HBox([truck_min_points, small_object_min_points], layout=item_layout1)
input_widgets9 = widgets.HBox([raydrop_range, apply_btn_range], layout=item_layout2)

input_widgets10 = widgets.HBox([starting_speed, jerk, deceleration])
input_widgets11 = widgets.HBox([T_latency, T_BB,], layout=item_layout1)
input_widgets12 = widgets.HBox([raydrop_distance, apply_btn_distance], layout=item_layout2)

input_widgets13 = widgets.HBox([excel_input1, excel_input2])
input_widgets15 = widgets.HBox([resolution1, sweep1], layout=item_layout1)
input_widgets16 = widgets.HBox([resolution2, sweep2], layout=item_layout1)
input_widgets14 = widgets.HBox([apply_btn_comparison_stop], layout=item_layout2)

# input_widgets15 = widgets.HBox([apply_btn_comparison_stop], layout=item_layout2)

tab = widgets.Tab([plot_output_first, plot_output_second, plot_output_third,
                   plot_output_seventh, plot_output_fourth, plot_output_fifth, plot_output_sixth], layout=item_layout2)
tab.set_title(0, 'Side View')
tab.set_title(1, 'Back View')
tab.set_title(2, '3D View')
tab.set_title(3, 'F1 Scores')
tab.set_title(4, 'Range Study')
tab.set_title(5, 'Stopping Distance Study')
tab.set_title(6, 'Comparison')

dashboard = widgets.VBox([input_widgets1, input_widgets2, input_widgets3, input_widgets4,
                          input_widgets5, input_widgets17, input_widgets18, input_widgets19,
                          input_widgets6, input_widgets7, input_widgets8,
                          input_widgets9, input_widgets10, input_widgets11,
                          input_widgets12, input_widgets13, input_widgets15, input_widgets16, input_widgets14,  tab])


