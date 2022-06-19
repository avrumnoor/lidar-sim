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



def plot(ped_min_points, bike_min_points, car_min_points, truck_min_points,
              small_object_min_points, small_object_y_slider, small_object_z_slider,
               object_size_dict, e1, l1, y_axis_scale, raydrop_range):


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

    data_distance = []
    object_size_dict['SmallObj'] = (small_object_y_slider, small_object_z_slider)
    for obj in object_size_dict:
        for i in range(200):
            t1= Target((i+1.81,0, 0), (4, object_size_dict[obj][0], object_size_dict[obj][1]))
            pc1 = PC(t1,e1,l1,0)
            data_distance.append([obj, i, pc1.get_filtered_points(object_size_dict[obj][0], object_size_dict[obj][1], 0).shape[0] * l1.sweep])

    plt.close('all')

    fig, ax = plt.subplots(nrows=5, sharex=True, figsize=(10,10))
    
    if raydrop_range.value == True:
        print('RAYDROP ON')
    else:
        print('RAYDROP OFF')
    
    for i,row in zip(range(5), ax):

        distance = [i[1] for i in data_distance[200 * i:200 * (i+1)]]
        
        
        number_of_points = [i[2] for i in data_distance[200*i:200 * (i+1)]]
        
#         print(number_of_points[80])
        
        
        if raydrop_range.value == True:
            
            number_of_points = apply_raydrop(number_of_points, distance, object_name_dict[i])
           

        range_req = calculate_range_req(number_of_points, min_points_dict[i])

        
        
        # fig=plt.figure(dpi=120)
        # ax=fig.add_subplot(111, label="1")

        

        row.plot(distance, number_of_points, color='k')
        row.set_xlabel("Distance (m)", color="k")
        row.set_ylabel("Number of Points", color="k")
        row.tick_params(axis='x', colors="k")
        row.tick_params(axis='y', colors="k")
        row.legend([data_distance[200 * i:200 * (i+1)][0][0]], loc='upper right')

        if range_req != "No detection":
            anchored_text = AnchoredText(f"Detection Range : {range_req} meters", loc='upper center')
        else:
            anchored_text = AnchoredText(f"Detection Range : {range_req}", loc='upper center')
        
        row.add_artist(anchored_text)

        row.axhline(y=min_points_dict[i], color='g', linestyle='dashed', linewidth='1')
        if isinstance(range_req, int):
            row.axvline(x=range_req, color='g', linestyle='dashed', linewidth='1')
            row.scatter(x=range_req, y=number_of_points[range_req], c='r')
        
        row.set_yscale(y_axis_scale)

    plt.show()


def calculate_range_req(number_of_points, min_points):
    try:
        position = [ n for n,i in enumerate(list(reversed(number_of_points))) if i >= min_points ][0]
    except:
        return "No detection"
    return len(number_of_points) -  position -1

