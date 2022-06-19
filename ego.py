
#defining the Ego vehicle class

class Ego:

    def __init__(self, E_coordinate, velocity, deceleration,Ego_dim):

        self.E_coordinate = E_coordinate

        self.velocity = velocity

        self.deceleration = deceleration

        self.Ego_dim = Ego_dim