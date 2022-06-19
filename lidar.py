
# defining the lidar class

class Lidar:

    def __init__(self,type,L_coordinate,elevation,azimuth_0, Lidar_dim, resolution, pos_hfov, neg_hfov, sweep):

        self.type = type

        self.L_coordinate = L_coordinate

        self.elevation = elevation

        self.azimuth_0 = azimuth_0

        self.Lidar_dim= Lidar_dim

        self.resolution= resolution

        # self.hfov = hfov

        self.pos_hfov = pos_hfov

        self.neg_hfov = neg_hfov

        self.sweep = sweep