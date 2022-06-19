#defining the PC - point cloud - class
import math
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import AnchoredText
import pandas as pd
from visualization3d import plotCubeAt2, Arrow3D
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
import random
import pickle
from sklearn.linear_model import LinearRegression
from surfel_disk_utilities import *

class PC:

    def __init__(self, target, ego, lidar, rd):

        self.target = target

        self.ego= ego

        self.lidar = lidar

        self.set_field_of_view()
        
        self.rd = rd



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


    def get_filtered_points(self, y, z, left_or_right):

        points = np.stack([self.get_all_y2(), self.get_all_z2()], axis=2)

        # print(points.shape)
        points = points.reshape(points.shape[0] * points.shape[1], 2)

        

        points = pd.DataFrame(points)

        points.columns = ['y', 'z']

        points['z'] = points['z'] + left_or_right

        points = points[(points['y'] >= 0) & (points['y'] <=y) & (points['z'] >=-z/2) & (points['z'] <=z/2)]

        return points



    def apply_raydrop(self, num_points, object_type):
        
        # LOAD THE MODEL
        pkl_filename = "./models/LR_all_car/LR_"+ object_type.value + ".pkl"
        with open(pkl_filename, 'rb') as file:
            linear_regressor = pickle.load(file)
        
        x_test = np.array([self.getdistance() ,  np.log10(num_points)]).reshape(1,-1)  
        
        rd_num_points = int(np.power(10,linear_regressor.predict(x_test)[0,0]))
                
        rd_ind = random.sample(range(0, num_points), rd_num_points)
        
        return rd_ind

#generates the plots

    def visuals_first(self, y, z, left_or_right, object_type):

        plt.close('all')

        xx = (self.target.T_coordinate[0]) * np.ones(len(self.get_y2()));

        

        AA = np.array([[self.lidar.L_coordinate[0] * np.ones(len(self.get_y2()))], [(self.target.T_coordinate[0]) * np.ones(len(self.get_y2()))]]).T;

        BB = np.array([[self.getheight() * np.ones(len(self.get_y2()))], [self.get_y2()]]).T;

        ss = np.hstack((AA))

        dd = np.hstack((BB))

        ss2 = np.ravel(ss).tolist()

        dd2 = np.ravel(dd).tolist()

        fig, ax = plt.subplots(dpi=120)

        ax.plot(xx, self.get_y2(), '*', ss2, dd2, color='blue', linewidth='0.5')
        
        plt.xlim([-10, 30])

        plt.ylim([-2, 10])

        ax.add_patch(Rectangle((self.lidar.L_coordinate[0] - self.ego.Ego_dim[0], 0 ), self.ego.Ego_dim[0], self.lidar.L_coordinate[1] - 0.3, color='#0099FF'))

        ax.add_patch(Rectangle((self.lidar.L_coordinate[0] - self.lidar.Lidar_dim[0], self.lidar.L_coordinate[1] - 0.3), 0.1, 0.3, color='red'))

        ax.add_patch(Rectangle((-20, -20), 200, 20, color='dimgrey', zorder=3))

        ax.add_patch(Rectangle((self.target.T_coordinate[0], 0), self.target.Target_dim[0], self.target.Target_dim[1], color='red'))

        ax.axhline(y=0, color='k', linestyle='solid', linewidth='2')

        ax.axhline(y=self.getheight(), color='b', linestyle='dashed', linewidth='1')
        
        number_of_rays = self.get_filtered_points(y,z, left_or_right).shape[0] * self.lidar.sweep
        
        print(y, z, left_or_right)
        
        if self.rd.value == True:
            
            rd_ind = self.apply_raydrop(number_of_rays, object_type)
            number_of_rays = len(rd_ind)
        
        anchored_text = AnchoredText("Number of points : {}".format(number_of_rays), loc=2)
        
#         file1 = open("res.txt","a")
#         file1.write(str(number_of_rays)+" \n")
        
        ax.add_artist(anchored_text)
        
        fig.suptitle('Side View', fontsize=16)
        plt.xlabel('Distance (m)', fontsize=14)
        plt.ylabel('Y axis (m)', fontsize=12)

        plt.show()

#         plt.close(fig)


    def visuals_second(self, y, z, left_or_right, object_type):

        # plt.close('all')

#         x = self.getdistance() * np.ones(len(self.get_y2()));

        

#         AA = np.array([[np.zeros(len(self.get_y2()))], [self.getdistance() * np.ones(len(self.get_y2()))]]).T;

#         BB = np.array([[self.getheight() * np.ones(len(self.get_y2()))], [self.get_y2()]]).T;

#         ss = np.hstack((AA))

#         dd = np.hstack((BB))

#         ss2 = np.ravel(ss).tolist()

#         dd2 = np.ravel(dd).tolist()

        fig, ax = plt.subplots(dpi=120)

        plt.plot(self.get_all_z2() + left_or_right, self.get_all_y2(),'o', markersize='0.2')
#         print(len(self.get_all_z2()))
#         print(len(self.get_all_y2()))

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
        
#         anchored_text = AnchoredText("Number of Points : {}".format(self.get_filtered_points(y,z, left_or_right).shape[0] * self.lidar.sweep), loc=2)
        
        number_of_rays = self.get_filtered_points(y,z, left_or_right).shape[0] * self.lidar.sweep
        
        if self.rd.value == True:
            
            rd_ind = self.apply_raydrop(number_of_rays, object_type)
            number_of_rays = len(rd_ind)
        
        anchored_text = AnchoredText("Number of points : {}".format(number_of_rays), loc=2)

        ax.add_artist(anchored_text)
        
        
        fig.suptitle('Back View', fontsize=16)
        plt.xlabel('Z axis (m)', fontsize=14)
        plt.ylabel('Y axis (m)', fontsize=12)

        plt.show()

        # plt.close(fig)



#     def visuals_third(self, y, z, left_or_right, object_type):

#         # plt.close('all')
#         points = self.get_filtered_points(y, z, left_or_right)

#         data_points = []
#         for index, row in points.iterrows():
#             data_points.append([[self.lidar.L_coordinate[0], self.target.T_coordinate[0]], [left_or_right, row['z']], [self.lidar.L_coordinate[1], row['y']]])


    

#         fig = plt.figure(figsize=(10,10))
#         ax = fig.gca(projection='3d')
#         ax.set_xlim3d(-3,30)
#         ax.set_ylim3d(-3, 3)
#         ax.set_zlim3d(0, 5)
#         ax.set_aspect("auto")

#         # ax.scatter([0.5], [0], [1.9], color="y", s=300)
# #         print(len(data_points))
# #         print(self.rd.value)
        
#         if self.rd.value == True:
            
#             rd_ind = self.apply_raydrop(len(data_points), object_type)
            
#             data_points = [data_points[i] for i in rd_ind]
            
            
        
# #         print(len(data_points))
        
#         for point in data_points:
#             a = Arrow3D(point[0], point[1], point[2], mutation_scale=20,
#                     lw=0.5, arrowstyle="-|>", color="k")
#             ax.add_artist(a)

#     #         ax.quiver(
#     #                 point[0][0], point[1][0], point[2][0], # <-- starting point of vector
#     #                 point[0][1] - point[0][0], point[1][1] - point[1][0],  point[2][1]- point[2][0], # <-- directions of vector
#     #                 color = 'red', alpha = .8, lw = 3,
#     # )

#         anchored_text = AnchoredText("Number of points : {}".format(len(data_points)* self.lidar.sweep), loc=2)

#         ax.add_artist(anchored_text)
        
#         ax.set_xlabel('X axis (m)')
#         ax.set_ylabel('Z axis (m)')
#         ax.set_zlabel('Y axis (m)')

#         positions = [(-3 + self.lidar.L_coordinate[0] ,-0.5 + left_or_right ,0), (self.target.T_coordinate[0],-z/2,0), (-0.5 + self.lidar.L_coordinate[0], -0.1 + left_or_right, self.lidar.L_coordinate[1] - 0.3)]
#         sizes = [(3,1, self.lidar.L_coordinate[1] - 0.3), (3,z,y), (0.5, 0.2, 0.3)]
#         colors = ["b", "crimson", "y"]
        
# #         positions = [(-3 + self.lidar.L_coordinate[0] ,-0.5 + left_or_right ,0), (-0.5 + self.lidar.L_coordinate[0], -0.1 + left_or_right, self.lidar.L_coordinate[1] - 0.3)]
# #         sizes = [(3,1, self.lidar.L_coordinate[1] - 0.3), (0.5, 0.2, 0.3)]
# #         colors = ["b", "y"]

#         plotcube = plotCubeAt2(positions,sizes,colors=colors, edgecolor="k")
#         ax.add_collection3d(plotcube)
# #         fig.suptitle('3d View', fontsize=16)

# #         surfel_disks(ax, "car_pc_v6.json", sz = 0.1, shift = [self.target.T_coordinate[0],0,0])
#         plt.show()
    
#         if self.rd.value == True:
#             print('RAYDROP ON')
#         else:
#             print('RAYDROP OFF')


###### WITH ASSET
    def visuals_third(self, y, z, left_or_right, object_type):

        # plt.close('all')
        points = self.get_filtered_points(y, z, left_or_right)

        data_points = []
        for index, row in points.iterrows():
            data_points.append([[self.lidar.L_coordinate[0], self.target.T_coordinate[0]+1], [left_or_right, row['z']], [self.lidar.L_coordinate[1], row['y']]])


    

        fig = plt.figure(figsize=(12,12))
        ax = fig.gca(projection='3d')
        ax.set_xlim3d(-3,30)
        ax.set_ylim3d(-3, 3)
        ax.set_zlim3d(0, 5)
        ax.set_aspect("auto")

        # ax.scatter([0.5], [0], [1.9], color="y", s=300)
#         print(len(data_points))
#         print(self.rd.value)
        
        if self.rd.value == True:
            
            rd_ind = self.apply_raydrop(len(data_points), object_type)
            
            data_points = [data_points[i] for i in rd_ind]
            
        
        def lineseg_dist(p, a, b):

            # normalized tangent vector
            d = np.divide(b - a, np.linalg.norm(b - a))

            # signed parallel distance components
            s = np.dot(a - p, d)
            t = np.dot(p - b, d)

            # clamped parallel distance
            h = np.maximum.reduce([s, t, np.zeros(len(p))])

            # perpendicular distance component
            c = np.cross(p - a, d)

#             return np.hypot(h, np.linalg.norm(c))
            return np.linalg.norm(c, axis=1)
        
#         print(len(data_points))
        
        surfel_disks(ax, "car_pc_v6.json", sz = 0.1, shift = [self.target.T_coordinate[0],0,0])
    
        asset_pc = get_pc("car_pc_v6.json")
        asset_pc[:,0] += self.target.T_coordinate[0]
        res_num = 0
        
        for point in data_points:
            
            point = np.array(point)
#             print(point)
#             print(asset_pc[0,:])
            dist_mat = lineseg_dist(asset_pc[:,:3], point[:,0], point[:,1])
            
#             print(min(dist_mat))
                
            filtered_asset_pc = asset_pc[dist_mat<0.05, :]
            filtered_asset_pc = filtered_asset_pc[filtered_asset_pc[:,0]<self.target.T_coordinate[0]+2]
                
            if len(filtered_asset_pc) > 0:
                res_num += 1
                closest_p_ind = np.argmin(filtered_asset_pc[:,0])

                a = Arrow3D([point[0][0], filtered_asset_pc[closest_p_ind,0]], [point[1][0], filtered_asset_pc[closest_p_ind,1]], [point[2][0], filtered_asset_pc[closest_p_ind,2]], mutation_scale=20, lw=0.5, arrowstyle="-|>", color="k",zorder=2)
                ax.add_artist(a)

    #         ax.quiver(
    #                 point[0][0], point[1][0], point[2][0], # <-- starting point of vector
    #                 point[0][1] - point[0][0], point[1][1] - point[1][0],  point[2][1]- point[2][0], # <-- directions of vector
    #                 color = 'red', alpha = .8, lw = 3,
    # )

        anchored_text = AnchoredText("Number of points : {}".format(res_num* self.lidar.sweep), loc=2)

        ax.add_artist(anchored_text)
        
        ax.set_xlabel('X axis (m)')
        ax.set_ylabel('Z axis (m)')
        ax.set_zlabel('Y axis (m)')

#         positions = [(-3 + self.lidar.L_coordinate[0] ,-0.5 + left_or_right ,0), (self.target.T_coordinate[0],-z/2,0), (-0.5 + self.lidar.L_coordinate[0], -0.1 + left_or_right, self.lidar.L_coordinate[1] - 0.3)]
#         sizes = [(3,1, self.lidar.L_coordinate[1] - 0.3), (3,z,y), (0.5, 0.2, 0.3)]
#         colors = ["b", "crimson", "y"]
        
        positions = [(-3 + self.lidar.L_coordinate[0] ,-0.5 + left_or_right ,0), (-0.5 + self.lidar.L_coordinate[0], -0.1 + left_or_right, self.lidar.L_coordinate[1] - 0.3)]
        sizes = [(3,1, self.lidar.L_coordinate[1] - 0.3), (0.5, 0.2, 0.3)]
        colors = ["b", "y"]

        plotcube = plotCubeAt2(positions,sizes,colors=colors, edgecolor="k")
        ax.add_collection3d(plotcube)
        ax.set_xlim(0,20);ax.set_ylim(-10,10);ax.set_zlim(-10,10)
#         fig.suptitle('3d View', fontsize=16)

#         surfel_disks(ax, "car_pc_v6.json", sz = 0.1, shift = [self.target.T_coordinate[0],0,0])
        plt.show()
    
        if self.rd.value == True:
            print('RAYDROP ON')
        else:
            print('RAYDROP OFF')

        



