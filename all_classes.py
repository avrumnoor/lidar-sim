
#defining the Target vehicle class
class Target:

    def __init__(self, T_coordinate, Target_dim):

        self.T_coordinate = T_coordinate

        self.Target_dim = Target_dim



#defining the Ego vehicle class

class Ego:

    def __init__(self, E_coordinate, velocity, deceleration,Ego_dim):

        self.E_coordinate = E_coordinate

        self.velocity = velocity

        self.deceleration = deceleration

        self.Ego_dim = Ego_dim



# defining the lidar class

class Lidar:

    def __init__(self,type,L_coordinate,elevation,azimuth_0, Lidar_dim, resolution, pos_hfov, neg_hfov):

        self.type = type

        self.L_coordinate = L_coordinate

        self.elevation = elevation

        self.azimuth_0 = azimuth_0

        self.Lidar_dim= Lidar_dim

        self.resolution= resolution

        # self.hfov = hfov

        self.pos_hfov = pos_hfov

        self.neg_hfov = neg_hfov


#defining the PC - point cloud - class
import numpy as np

import matplotlib.pyplot as plt

import math

from matplotlib.patches import Rectangle
from matplotlib.offsetbox import AnchoredText
import pandas as pd

from visualization3d import plotCubeAt2, Arrow3D
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

class PC:

    def __init__(self, target, ego, lidar):

        self.target = target

        self.ego= ego

        self.lidar = lidar

        self.set_field_of_view()



#finds the distance between ego and target using their coordinates

    def getdistance(self):

        # print('salam')

        d = abs(self.target.T_coordinate[0] - self.lidar.L_coordinate[0]);

        return d



#finds the height of the lidar tip from the ground (could be defined better)

    def getheight(self):
        
        h = abs(self.target.T_coordinate[1] - self.lidar.L_coordinate[1]);

        return h



#finds the y2(vertical) coordinate of one laser beam on the target

    def get_y2(self):

        y2 = self.getheight() + self.getdistance() * np.tan(self.lidar.elevation * math.pi / 180);

        return y2


    def get_filtered_y2(self):

        y2 = self.getheight() + self.getdistance() * np.tan(self.lidar.elevation * math.pi / 180);
        y2 = y2[ (y2 >=0) * (y2 <= self.target.Target_dim[1])]

        return y2



#finds the z2(horizontal) coordinate of one laser beam on the target

    def get_z2(self):

        z2 = self.getdistance()* np.tan(self.lidar.azimuth_0 * math.pi / 180)

        return z2


    def get_filtered_z2(self):

        z2 = self.getdistance()* np.tan(self.lidar.azimuth_0 * math.pi / 180)
        z2 = z2[ (z2 >=0) * (z2 <= self.target.Target_dim[2])]

        return z2



#finds the z2(horizontal) coordinate of all laser beams on the target when swiping the hfov (lidar horizontal field of view)

    def set_field_of_view(self):


        inc_pos = np.arange(0, self.lidar.pos_hfov + self.lidar.resolution, self.lidar.resolution);

        inc_neg = np.arange(0, -self.lidar.neg_hfov  - self.lidar.resolution, -self.lidar.resolution);

        inc_tot = np.concatenate((np.flip(inc_pos), inc_neg[1:]));

        self.num_tot = inc_tot

    def get_all_z2(self):



        # inc_pos = np.arange(0, self.lidar.hfov / 2 + self.lidar.resolution, self.lidar.resolution);

        # inc_neg = np.arange(0, -self.lidar.hfov / 2 - self.lidar.resolution, -self.lidar.resolution);

        # inc_tot = np.concatenate((np.flip(inc_pos), inc_neg[1:]));

        # self.num_tot = len(inc_tot)

        inc_tot = self.num_tot

        all_z2 =np.zeros((len(self.lidar.azimuth_0),1)).reshape(-1,1)

        for inc in inc_tot:

            inc_z2 = self.getdistance()* np.tan((self.lidar.azimuth_0 + inc) * math.pi / 180).reshape(-1,1)

            all_z2 = np.append(all_z2, inc_z2, axis=1)

        all_z2 = np.delete(all_z2, 0, 1)  # delete second column of C
        
#         print(all_z2.shape)

        return all_z2



# finds the y2(vertical) coordinate of all laser beams - they're identical through each resolution increment - on the target when swiping the hfov (lidar horizontal field of view)

    def get_all_y2(self):

        # y2_slice_num= int(self.lidar.hfov /self.lidar.resolution +1) #should be called as len(inc_tot)
        
        # if y2_slice_num % 2 == 0:
        #     y2_slice_num+=1

        y2_slice_num = len(self.num_tot)

        inc_y2= self.get_y2().reshape(-1,1)

        all_y2 = np.zeros((len(inc_y2),1))

        for i in range(y2_slice_num):

            all_y2 = np.append(all_y2, inc_y2, axis=1)



        all_y2 = np.delete(all_y2, 0, 1)  # delete second column of C
        
#         print(all_y2.shape)

        return all_y2


    def get_filtered_points(self, y, z):

        points = np.stack([self.get_all_y2(), self.get_all_z2()], axis=2)

        # print(points.shape)
        points = points.reshape(points.shape[0] * points.shape[1], 2)

        

        points = pd.DataFrame(points)

        points.columns = ['y', 'z']

        points = points[(points['y'] >= 0) & (points['y'] <=y) & (points['z'] >=-z/2) & (points['z'] <=z/2)]

        return points






#generates the plots

    def visuals_first(self, y, z):

        plt.close('all')

        xx = self.getdistance() * np.ones(len(self.get_y2()));

        

        AA = np.array([[np.zeros(len(self.get_y2()))], [self.getdistance() * np.ones(len(self.get_y2()))]]).T;

        BB = np.array([[self.getheight() * np.ones(len(self.get_y2()))], [self.get_y2()]]).T;

        ss = np.hstack((AA))

        dd = np.hstack((BB))

        ss2 = np.ravel(ss).tolist()

        dd2 = np.ravel(dd).tolist()

        fig, ax = plt.subplots(dpi=200)

        ax.plot(xx, self.get_y2(), '*', ss2, dd2, color='blue', linewidth='0.5')

        plt.xlim([-10, 105])

        plt.ylim([-2, 10])

        ax.add_patch(Rectangle((0 - self.ego.Ego_dim[0], 0 - self.ego.Ego_dim[1] - self.lidar.Lidar_dim[1] + self.getheight()), self.ego.Ego_dim[0], self.ego.Ego_dim[1], color='#0099FF'))

        ax.add_patch(Rectangle((0 - self.lidar.Lidar_dim[0], self.getheight() - self.lidar.Lidar_dim[1]), .1, .2, color='red'))

        ax.add_patch(Rectangle((-20, -20), 200, 20, color='dimgrey', zorder=3))

        ax.add_patch(Rectangle((self.getdistance(), 0), self.target.Target_dim[0], self.target.Target_dim[1], color='red'))

        ax.axhline(y=0, color='k', linestyle='solid', linewidth='2')

        ax.axhline(y=self.getheight(), color='b', linestyle='dashed', linewidth='1')

        anchored_text = AnchoredText("Number of points : {}".format(self.get_filtered_points(y,z).shape[0]), loc=2)
        
        ax.add_artist(anchored_text)
        
        fig.suptitle('Side View', fontsize=16)
        plt.xlabel('distance (m)', fontsize=14)
        plt.ylabel('Y axis (m)', fontsize=12)

        plt.show()

        # plt.close(fig)


    def visuals_second(self, y, z):

        # plt.close('all')    

#         x = self.getdistance() * np.ones(len(self.get_y2()));

        

#         AA = np.array([[np.zeros(len(self.get_y2()))], [self.getdistance() * np.ones(len(self.get_y2()))]]).T;

#         BB = np.array([[self.getheight() * np.ones(len(self.get_y2()))], [self.get_y2()]]).T;

#         ss = np.hstack((AA))

#         dd = np.hstack((BB))

#         ss2 = np.ravel(ss).tolist()

#         dd2 = np.ravel(dd).tolist()

        fig, ax = plt.subplots(dpi=200)

        plt.plot(self.get_all_z2(), self.get_all_y2(),'o', markersize='0.2')
#         print(self.get_all_z2())
#         print(self.get_all_y2())

#         y = pd.DataFrame(self.get_all_y2())
#         label = list(range(128))

#         for i,j,z in zip(self.get_all_z2(), self.get_all_y2(), label):
# #             corr = -1.7 # adds a little correction to put annotation in marker's centrum
#             if z < 10:
#                 ax.annotate(z,  xy=(i + -1.1 , j - 0.5), fontsize=4)
#             elif z < 100:
#                 ax.annotate(z,  xy=(i + -1.33 , j - 0.5), fontsize=4)
#             else:
#                 ax.annotate(z,  xy=(i + -1.7 , j - 0.5), fontsize=4)
                

        plt.xlim([-5, 5])

        plt.ylim([-2, 10])

        ax.add_patch(Rectangle((-20, -20), 40, 20, color='dimgrey', zorder=3))

        ax.add_patch(Rectangle((0-self.target.Target_dim[2]/2, 0), self.target.Target_dim[2], self.target.Target_dim[1], color='red'))

        ax.axhline(y=0, color='k', linestyle='solid', linewidth='2')

        ax.axhline(y=self.getheight(), color='b', linestyle='dashed', linewidth='1')

        ax.axvline(x=0, color='b', linestyle='dashed', linewidth='1')
        
        anchored_text = AnchoredText("Number of points : {}".format(self.get_filtered_points(y,z).shape[0]), loc=2)

        ax.add_artist(anchored_text)
        
        
        fig.suptitle('Back View', fontsize=16)
        plt.xlabel('Z axis (m)', fontsize=14)
        plt.ylabel('Y axis (m)', fontsize=12)

        plt.show()

        # plt.close(fig)



    def visuals_third(self, y, z):

        # plt.close('all')
        points = self.get_filtered_points(y, z)

        data_points = []
        for index, row in points.iterrows():
            data_points.append([[0, self.target.T_coordinate[0]], [0, row['z']], [1.842, row['y']]])


    

        fig = plt.figure(figsize=(10,10))
        ax = fig.gca(projection='3d')
        ax.set_xlim3d(-3,105)
        ax.set_ylim3d(-3, 5)
        ax.set_zlim3d(0, 5)
        ax.set_aspect("auto")

        ax.scatter([0.5], [0], [1.842], color="y", s=300)

        for point in data_points:
            a = Arrow3D(point[0], point[1], point[2], mutation_scale=20,
                    lw=0.5, arrowstyle="-|>", color="k")
            ax.add_artist(a)

    #         ax.quiver(
    #                 point[0][0], point[1][0], point[2][0], # <-- starting point of vector
    #                 point[0][1] - point[0][0], point[1][1] - point[1][0],  - point[2][0], # <-- directions of vector
    #                 color = 'red', alpha = .8, lw = 3,
    # )

        ax.set_xlabel('X axis (m)')
        ax.set_ylabel('Z axis (m)')
        ax.set_zlabel('Y axis (m)')

        positions = [(-3,-0.5,0), (self.target.T_coordinate[0],-z/2,0)]
        sizes = [(3,1,1.841), (3,z,y)]
        colors = ["crimson","limegreen"]

        plotcube = plotCubeAt2(positions,sizes,colors=colors, edgecolor="k")
        ax.add_collection3d(plotcube)

        plt.show()

        



