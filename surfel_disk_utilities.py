from mpl_toolkits.mplot3d import axes3d
from matplotlib.patches import Circle, PathPatch
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
from mpl_toolkits.mplot3d import art3d
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json

# def plot_vector(fig, orig, v, color='blue'):
#    ax = fig.gca(projection='3d')
#    orig = np.array(orig); v=np.array(v)
#    ax.quiver(orig[0], orig[1], orig[2], v[0], v[1], v[2],color=color)
#    ax.set_xlim(0,10);ax.set_ylim(0,10);ax.set_zlim(0,10)
#    ax = fig.gca(projection='3d')  
#    return fig

def rotation_matrix(d):
    sin_angle = np.linalg.norm(d)
    if sin_angle == 0:return np.identity(3)
    d /= sin_angle
    eye = np.eye(3)
    ddt = np.outer(d, d)
    skew = np.array([[    0,  d[2],  -d[1]],
                  [-d[2],     0,  d[0]],
                  [d[1], -d[0],    0]], dtype=np.float64)

    M = ddt + np.sqrt(1 - sin_angle**2) * (eye - ddt) + sin_angle * skew
    return M

def pathpatch_2d_to_3d(pathpatch, z, normal):
    if type(normal) is str: #Translate strings to normal vectors
        index = "xyz".index(normal)
        normal = np.roll((1.0,0,0), index)

    normal /= np.linalg.norm(normal) #Make sure the vector is normalised
    path = pathpatch.get_path() #Get the path and the associated transform
    trans = pathpatch.get_patch_transform()

    path = trans.transform_path(path) #Apply the transform

    pathpatch.__class__ = art3d.PathPatch3D #Change the class
    pathpatch._code3d = path.codes #Copy the codes
    pathpatch._facecolor3d = pathpatch.get_facecolor #Get the face color    

    verts = path.vertices #Get the vertices in 2D

    d = np.cross(normal, (0, 0, 1)) #Obtain the rotation vector    
    M = rotation_matrix(d) #Get the rotation matrix

    pathpatch._segment3d = np.array([np.dot(M, (x, y, 0)) + (0, 0, z) for x, y in verts])

def pathpatch_translate(pathpatch, delta):
    pathpatch._segment3d += delta

def plot_plane(ax, point, normal, size=10, color='y'):  
    cms = plt.cm
    c = cms.jet(point[3])
    p = Circle((0, 0), size, facecolor = c, alpha = .2, zorder = 1)
    ax.add_patch(p)
    pathpatch_2d_to_3d(p, z=0, normal=normal)
    pathpatch_translate(p, (point[0], point[1], point[2]))


# o = np.array([5,5,5])
# v = np.array([3,3,3])
# n = [0.5, 0.5, 0.5]

# def surfel_disks(pc, normals, sz = 0.05):
#     fig = plt.figure(figsize = (12, 10))
#     ax = fig.gca(projection='3d')  
    
#     pc[:,3] = pc[:,3] / max(pc[:,3])
    
#     for ind in range(0, len(pc)):
#         plot_plane(ax, pc[ind,:], normals[ind,:], size=sz)    
#     ax.set_xlim(-10,10);ax.set_ylim(-10,10);ax.set_zlim(-10,10)
#     plt.show()
   
def get_pc(filename):
    
    file = open(filename, "r")
    pc_dict_info = json.load(file)
    
    pc = np.array(pc_dict_info['pc'])
    
    temp = np.copy(pc[:,0])
    pc[:,0] = pc[:,1]
    pc[:,1] = temp
    
    return pc
    
def surfel_disks(ax, filename, sz = 0.05, shift = [0,0,0]):
    
    file = open(filename, "r")
    pc_dict_info = json.load(file)
    
    pc = np.array(pc_dict_info['pc'])
    normals = np.array(pc_dict_info['normals'])
    
    temp = np.copy(pc[:,0])
    pc[:,0] = pc[:,1]
    pc[:,1] = temp
    
    temp = np.copy(normals[:,0])
    normals[:,0] = normals[:,1]
    normals[:,1] = temp
    
#     fig = plt.figure(figsize = (12, 10))
#     ax = fig.gca(projection='3d')  
    
    pc[:,3] = pc[:,3] / max(pc[:,3])
    pc[:,:3] = pc[:,:3] + np.array(shift) 
    
    for ind in range(0, len(pc)):
        plot_plane(ax, pc[ind,:], normals[ind,:], size=sz)    
#     ax.set_xlim(0,20);ax.set_ylim(-10,10);ax.set_zlim(-10,10)
#     plt.show()

def surfel_disks_v2(ax, filename, sz = 0.05, shift = [0,0,0]):
    
    file = open(filename, "r")
    pc_dict_info = json.load(file)
    
    pc = np.array(pc_dict_info['pc'])
    normals = np.array(pc_dict_info['normals'])
    
    temp = np.copy(pc[:,0])
    pc[:,0] = pc[:,1]
    pc[:,1] = temp
    
    temp = np.copy(normals[:,0])
    normals[:,0] = normals[:,1]
    normals[:,1] = temp
    
#     fig = plt.figure(figsize = (12, 10))
#     ax = fig.gca(projection='3d')  
    
    pc[:,3] = pc[:,3] / max(pc[:,3])
    pc[:,:3] = pc[:,:3] + np.array(shift) 
    
    for ind in range(0, len(pc)):
        plot_plane(ax, pc[ind,:], normals[ind,:], size=sz)    
    ax.set_xlim(0,20);ax.set_ylim(-10,10);ax.set_zlim(-10,10)
    ax.view_init(0, 90)
#     plt.show()
