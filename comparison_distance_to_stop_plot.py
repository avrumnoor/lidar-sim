import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression

def plot_stop_distance(distance):

    fig, ax = plt.subplots(dpi=120)
    plt.xlim([-10, 300])
    plt.ylim([-2, 10])
    ax.add_patch(Rectangle((-8,0), 8, 4, color='blue'))
    ax.plot([0, distance], [0,0], 'ro-', color='red', linewidth='10')
    ax.add_patch(Rectangle((distance, 0), 8, 4, color='green'))
    ax.axhline(y=0, color='k', linestyle='solid', linewidth='2')
    anchored_text = AnchoredText("Stopping Distance : {:.2f} (m)".format(distance), loc=2)
    ax.add_artist(anchored_text)
    
    fig.suptitle('Stopping Distance', fontsize=16)
    plt.xlabel('Distance (m)', fontsize=14)
    plt.ylabel('Y axis (m)', fontsize=12)

    plt.show()



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


# fig, ax = plt.subplots(figsize=(8,6))



def plot_comparison_stop(distance_points1, distance_points2, ped_min_points, bike_min_points, car_min_points,
                       truck_min_points, small_object_min_points, y_axis_scale, raydrop_distance):


#     plt.close('all')


#     fig = plt.figure(facecolor='white', figsize=(12,5))
#     ax1 = fig.add_subplot(111)

    # ['object_type', 'speed', 'distance', 'number_of_points']

    min_points_dict = {
        "Pedestrian": ped_min_points,
        "Motorcycle": bike_min_points,
        "Car": car_min_points,
        "Truck": truck_min_points,
        "SmallObj": small_object_min_points
    }
    
    object_name_dict = {
    0: "Pedestrian",
    1: "Bike",
    2: "Car",
    3: "Truck",
    4: "Small_Object"
    }

    if raydrop_distance.value == True:
        print('RAYDROP ON')
    else:
        print('RAYDROP OFF')

    string = 'Speed Reqs (mph)\n\n'
    string += '                     L1:     L2:    Diff(%):   \n'

    colors = ['#12B4FB', '#FC6140', '#12FB24', 'tab:brown', '#fcba03']


#     fig, ax = plt.subplots(nrows=5, sharex=True, figsize=(12,12))
#     fig.tight_layout(pad=7.0)
    
    final_string1 = '\n\n Speed Requirement (mph)\n\n'
    final_string1 += "{0:<18}{1:<10}{2:<10}{3:<10} \n".format(' ', 'LiDAR 1', 'LiDAR 2','Diff (%)')
    min_diff = 100
    sign = 1
    
    fig, ax = plt.subplots(nrows=5, sharex=True, figsize=(12,12))
    fig.tight_layout(pad=7.0)
    
    
    
    for i,row in zip(range(5), ax):
                
        s_ind = 81*i
        e_ind = (81*(i+1))
        
        number_of_points1 = distance_points1[s_ind:e_ind,3].astype(np.float)
        distance1 = distance_points1[s_ind:e_ind,2].astype(np.float)
        range_req1 = calculate_range_req(number_of_points1, min_points_dict[distance_points1[s_ind,0]])
        
        number_of_points2 = distance_points2[s_ind:e_ind,3].astype(np.float)
        distance2 = distance_points2[s_ind:e_ind,2].astype(np.float)
        range_req2 = calculate_range_req(number_of_points2, min_points_dict[distance_points2[s_ind,0]])
        
        row.axhline(y=min_points_dict[distance_points1[s_ind,0]], color='g', linestyle='dashed', linewidth='1')
        
        row.plot(distance_points1[s_ind:e_ind,1], number_of_points1, label='Lidar 1', color='k', zorder = 1)
        row.plot(distance_points2[s_ind:e_ind,1], number_of_points2, label='Lidar 2', color='r', zorder = 1)
        
        if isinstance(range_req1, int) and isinstance(range_req2, int):
            diff = 100*round((max(range_req1, range_req2)-min(range_req1, range_req2))/max(range_req1, range_req2),3)
            if diff > 0 and diff < min_diff:
                min_diff = min(diff, min_diff)
                
                if range_req1 < range_req2:
                    sign = -1
                else:
                    sign = 1
                
            diff = str(format(diff, ".1f"))
        else:
            diff = 'N/A'
            
        
#         final_string1 += "{0:<18}{1:<10}{2:<10}{3:<10} \n".format(str(object_name_dict[i]),str(range_req1),str(range_req2), diff)
        
        if isinstance(range_req1, int) and len(number_of_points1) > range_req1:
            row.axvline(x=range_req1, color='g', linestyle='dashed', linewidth='1')
            row.scatter(x=range_req1, y=number_of_points1[range_req1], c='g', zorder = 2) 
        else:
            range_req1 = 'N/A'
            diff = 'N/A'
            
        if isinstance(range_req2, int)and len(number_of_points2) > range_req2:
            row.axvline(x=range_req2, color='g', linestyle='dashed', linewidth='1')
            row.scatter(x=range_req2, y=number_of_points2[range_req2], c='g', zorder = 2) 
        else:
            range_req2 = 'N/A'
            diff = 'N/A'
        
        final_string1 += "{0:<18}{1:<10}{2:<10}{3:<10} \n".format(str(object_name_dict[i]),str(range_req1),str(range_req2), diff)
        
        row.set_title(distance_points1[s_ind,0])
#         row.set_xlim(0, 60)
        leg = row.legend(loc='upper right', prop={'size': 10})

        row.set_xlabel("Starting Speed (mph)")
        row.set_ylabel("Number of Points")
        row.set_yscale(y_axis_scale)
        

        row2 = row.twiny()
        row2.set_xlabel("Stopping Distance (m)")
        row2.set_xlim(0, 80)
        row2.set_xlim(row.get_xlim())
        speed = distance_points1[s_ind:e_ind,1].astype(np.float).tolist()
        speed = [round(speed[j]) for j in [10,20,30,40,50,60,70,80]]
        distance = distance1.tolist()
        distance = [round(distance[j]) for j in [10,20,30,40,50,60,70,80]]
               
        row2.set_xticks(speed)
        row2.set_xticklabels(distance)
        
        row.set_xticks(speed)
        row.set_xticklabels(speed)

#     side_text = plt.figtext(0.93, 0.5, , bbox=dict(facecolor='white'))
# f   plt.subplots_adjust(top=0.8)

#     plt.gcf().text(0.8, 0.4, string, fontsize=12, bbox=dict(facecolor='white'))
#     plt.subplots_adjust(right=0.7)

    if min_diff < 100:
        if sign == 1:
            final_string1 += '\n' + 'Ego vehicle can drive at least by ' + str(format(min_diff, ".1f")) + '% faster with Lidar #1. ' 
        else:
            final_string1 += '\n' + 'Ego vehicle can drive at least by ' + str(format(min_diff, ".1f")) + '% faster with Lidar #2. ' 
    
    plt.show()
    print(final_string1)




def calculate_range_req(number_of_points, min_points):
    try:
        position = [ n for n,i in enumerate(list(reversed(number_of_points))) if i >= min_points ][0]
    except:
        return "N/A"
    return len(number_of_points) -  position



