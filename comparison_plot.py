from target import Target
from pointcloud import PC
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression


def apply_raydrop(num_points, distance, object_type):

    # LOAD THE MODEL
    pkl_filename = "./models/LR/LR_"+ object_type +".pkl"
    with open(pkl_filename, 'rb') as file:
        linear_regressor = pickle.load(file)

    temp_dist = np.expand_dims(np.array(distance),axis=1)
    temp_num = np.expand_dims(np.log10(np.array(num_points)+1),axis=1)
    
    x_test = np.concatenate([temp_dist , temp_num ], axis = 1)
    
    rd_num_points = np.power(10,linear_regressor.predict(x_test))
    
    rd_num_points.astype(int)

    return rd_num_points


def data_point_generation_range(i, data_distance, raydrop_range, object_name_dict, min_points_dict):
    
    distance = [i[1] for i in data_distance[200 * i:200 * (i+1)]]
        
        
    number_of_points = [i[2] for i in data_distance[200 * i:200 * (i+1)]]


    if raydrop_range.value == True:

        number_of_points = apply_raydrop(number_of_points, distance, object_name_dict[i])


    range_req = calculate_range_req(number_of_points, min_points_dict[i])
    
    return distance, number_of_points, range_req
    
    

def plot_range(ped_min_points, bike_min_points, car_min_points, truck_min_points,
              small_object_min_points, small_object_y_slider, small_object_z_slider,
               object_size_dict, e1, l1, l2, y_axis_scale, raydrop_range):


    min_points_dict = {
        0: ped_min_points,
        1: bike_min_points,
        2: car_min_points,
        3: truck_min_points,
        4: small_object_min_points
    }
    
    object_name_dict = {
    0: "Pedestrian",
    1: "Bike",
    2: "Car",
    3: "Truck",
    4: "Small_Object"
    }
    
    space_num_dict = {
    0: "Pedestrian  ",
    1: "Bike            ",
    2: "Car             ",
    3: "Truck           ",
    4: "Small_Object"
    }

    data_distance1 = []
    data_distance2 = []
    object_size_dict['SmallObj'] = (small_object_y_slider, small_object_z_slider)
    
    final_string1 = '\n\n Range Comparison (m)\n\n'
    final_string1 += "{0:<18}{1:<10}{2:<10}{3:<10} \n".format(' ', 'LiDAR 1', 'LiDAR 2','Diff (%)')
    min_diff = 100
    sign = 1
    for obj in object_size_dict:
        for i in range(200):
            t1= Target((i+1.81,0, 0), (4, object_size_dict[obj][0], object_size_dict[obj][1]))
            pc1 = PC(t1,e1,l1,0)
            data_distance1.append([obj, i, pc1.get_filtered_points(object_size_dict[obj][0], object_size_dict[obj][1], 0).shape[0] * l1.sweep])
            
            pc2 = PC(t1,e1,l2,0)
            data_distance2.append([obj, i, pc2.get_filtered_points(object_size_dict[obj][0], object_size_dict[obj][1], 0).shape[0] * l2.sweep])
            
    plt.close('all')

    fig, ax = plt.subplots(nrows=5, sharex=True, figsize=(10,10))
    fig.tight_layout(pad=3.0)
    
    if raydrop_range.value == True:
        print('RAYDROP ON')
    else:
        print('RAYDROP OFF')
    
    for i,row in zip(range(5), ax):

        distance1, number_of_points1, range_req1 = data_point_generation_range(i,data_distance1, raydrop_range, object_name_dict, min_points_dict)
        
             
        
        distance2, number_of_points2, range_req2 = data_point_generation_range(i,data_distance2, raydrop_range, object_name_dict, min_points_dict)
        
        if isinstance(range_req1, int) and isinstance(range_req2, int) :
            diff = 100*round((max(range_req1, range_req2)-min(range_req1, range_req2))/max(range_req1, range_req2),3)
            
            if diff > 0:
                min_diff = min(diff, min_diff)
            diff = str(format(diff, ".1f"))
            
            if range_req1 != range_req2:
                sign = (range_req1-range_req2) / abs(range_req1-range_req2)
        else:
            diff = 'N/A'
            
        
        final_string1 += "{0:<18}{1:<10}{2:<10}{3:<10} \n".format(str(space_num_dict[i]),str(range_req1),str(range_req2), diff)
        row.plot(distance1, number_of_points1, color='k', label = 'Lidar 1')
        row.plot(distance2, number_of_points2, color='r', label = 'Lidar 2')
        row.set_xlabel("Distance (m)", color="k")
        row.set_ylabel("Number of Points", color="k")
        row.set_title(object_name_dict[i])
        row.tick_params(axis='x', colors="k")
        row.tick_params(axis='y', colors="k")
        row.legend(loc = 'upper right')
#         row.legend([data_distance1[200 * i:200 * (i+1)][0][0]], loc='upper right')

#         if range_req1 != "N\A":
#         anchored_text = AnchoredText(f"Lidar 1 Range : {range_req1} m, Lidar 2 Range : {range_req2} m", loc='upper center')
#         else:
#             anchored_text = AnchoredText(f"Lidar 1 Range : {range_req1}, Lidar 2 Range : {range_req2}", loc='upper center')
        
#         row.add_artist(anchored_text)    
        
        row.axhline(y=min_points_dict[i], color='g', linestyle='dashed', linewidth='1')
        
        if isinstance(range_req1, int):
            row.axvline(x=range_req1, color='k', linestyle='dashed', linewidth='1')
            row.scatter(x=range_req1, y=number_of_points1[range_req1], c='g')
        
        if isinstance(range_req2, int):
            row.axvline(x=range_req2, color='r', linestyle='dashed', linewidth='1')
            row.scatter(x=range_req2, y=number_of_points2[range_req2], c='g')
        
        row.set_yscale(y_axis_scale)

        
#     plt.gcf().text(0.75, 0.1, final_string1, fontsize=10, bbox=dict(facecolor='white'))
#     plt.subplots_adjust(right=0.7)
    
    
    if min_diff < 100:
        if sign == 1:
            final_string1 += '\n' + 'Lidar #1 has a wider range by at least ' + str(format(min_diff, ".1f")) + '%'
        else:
            final_string1 += '\n' + 'Lidar #2 has a wider range by at least ' + str(format(min_diff, ".1f")) + '%'
    
    plt.show()
    print(final_string1)


def calculate_range_req(number_of_points, min_points):
    try:
        position = [ n for n,i in enumerate(list(reversed(number_of_points))) if i >= min_points ][0]
    except:
        return "N/A"
    return len(number_of_points) -  position -1

