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



def plot(distance_points, ped_min_points, bike_min_points, car_min_points,
                       truck_min_points, small_object_min_points, y_axis_scale, raydrop_distance):


    plt.close('all')


    fig = plt.figure(facecolor='white', figsize=(12,5))
    ax1 = fig.add_subplot(111)

    # ['object_type', 'speed', 'distance', 'number_of_points']

    min_points_dict = {
        "Pedestrian": ped_min_points,
        "Motorcycle": bike_min_points,
        "Car": car_min_points,
        "Truck": truck_min_points,
        "SmallObj": small_object_min_points
    }
    
    object_name_dict = {
    "Pedestrian": "Pedestrian",
    "Motorcycle": "Bike",
    "Car": "Car",
    "Truck": "Truck",
    "SmallObj": "Small_Object"
    }

    if raydrop_distance.value == True:
        print('RAYDROP ON')
    else:
        print('RAYDROP OFF')

    string = 'Speed Reqs (mph)\n\n'

    colors = ['#12B4FB', '#FC6140', '#12FB24', 'tab:brown', '#fcba03']
    for label, df in distance_points.groupby('object_type'):
    #     print(df.columns)
    #     df = df[['distance', 'Number of Points']]
        # print(label, df['number_of_points'].tolist())
        number_of_points = df['number_of_points'].tolist()
        distance = df['distance'].tolist()
        
#         print(number_of_points)
        
        if raydrop_distance.value == True:
            
            number_of_points = apply_raydrop(number_of_points, distance, object_name_dict[label])
        
        range_req = calculate_range_req(number_of_points, min_points_dict[label])
        string += str(label) + ': ' + str(range_req) + '\n'
        ax1.axhline(y=min_points_dict[label], color='g', linestyle='dashed', linewidth='1')
        ax1.plot(df['speed'], number_of_points, linewidth=4, label=label, color=colors.pop(0), zorder = 1)
        if isinstance(range_req, int) and range_req < len(number_of_points):
            ax1.axvline(x=range_req, color='g', linestyle='dashed', linewidth='1')
#             ax1.scatter(x=range_req, y=df['number_of_points'].tolist()[range_req], c='r') 
            ax1.scatter(x=range_req, y=number_of_points[range_req], c='r',zorder=2) 
#         ax1.plot(df['speed'], df['number_of_points'], linewidth=4, label=label, color=colors.pop(0))
        
#         ax1.plot(df['speed'], df['number_of_points'], linewidth=4, label=label, color=colors[3])

    ax1.set_xlim(0, 80)
    leg = plt.legend(loc='upper right', prop={'size': 15})

    ax1.set_xlabel("Starting Speed (mph)")
    ax1.set_ylabel("Number of Points")
    ax1.set_yscale(y_axis_scale)
    

    ax2 = ax1.twiny()
    ax2.set_xlabel("Stopping Distance (m)")
    ax2.set_xlim(0, 60)
    speed = df['speed'].tolist()
    speed = [round(speed[i], 2) for i in [10,20,30,40,50,60]]
    distance = df['distance'].tolist()
    distance = [round(distance[i],2) for i in [10,20,30,40,50,60]]
    
    ax2.set_xticks(speed)
    ax2.set_xticklabels(distance)

#     side_text = plt.figtext(0.93, 0.5, , bbox=dict(facecolor='white'))
# f   plt.subplots_adjust(top=0.8)

    plt.gcf().text(0.8, 0.4, string, fontsize=12, bbox=dict(facecolor='white'))
    plt.subplots_adjust(right=0.7)

    plt.show()
    print(string)




def calculate_range_req(number_of_points, min_points):
    try:
        position = [ n for n,i in enumerate(list(reversed(number_of_points))) if i >= min_points ][0]
    except:
        return "No detection"
    return len(number_of_points) -  position



