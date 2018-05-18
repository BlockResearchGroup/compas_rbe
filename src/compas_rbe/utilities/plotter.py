import numpy as np
import scipy as sp
import pylab as pl

import mpl_toolkits.mplot3d as a3
import matplotlib.pyplot as plt
from itertools import product, combinations
import matplotlib.colors as colors

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):
    """ http://stackoverflow.com/questions/11140163/python-matplotlib-plotting-a-3d-cube-a-sphere-and-a-vector
    """

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def rotation_matrix(d):
    """
    http://stackoverflow.com/questions/18228966/how-can-matplotlib-2d-patches-be-transformed-to-3d-with-arbitrary-normals

    Calculates a rotation matrix given a vector d. The direction of d
    corresponds to the rotation axis. The length of d corresponds to
    the sin of the angle of rotation.

    Variant of: http://mail.scipy.org/pipermail/numpy-discussion/2009-March/040806.html
    """
    sin_angle = np.linalg.norm(d)

    if sin_angle == 0:
        return np.identity(3)

    d /= sin_angle

    eye = np.eye(3)
    ddt = np.outer(d, d)
    skew = np.array(
        [[0, d[2], -d[1]],
         [-d[2], 0, d[0]],
         [d[1], -d[0], 0]], dtype=np.float64)

    M = ddt + np.sqrt(1 - sin_angle**2) * (eye - ddt) + sin_angle * skew
    return M


def pathpatch_2d_to_3d(pathpatch, z=0, normal='z'):
    """
    Transforms a 2D Patch to a 3D patch using the given normal vector.
    The patch is projected into they XY plane, rotated about the origin
    and finally translated by z.
    """
    if isinstance(normal, str): 
        # Translate strings to normal vectors
        index = "xyz".index(normal)
        normal = np.roll((1,0,0), index)

    #normal /= norm(normal) #Make sure the vector is normalised

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
    """
    Translates the 3D pathpatch by the amount delta.
    """
    pathpatch._segment3d += delta

def randrange(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

    
def view_all(block_model,blocks, scale, t_scale, v_scale , xlim=[-1,1], ylim=[-1,1], zlim=[0,1]):   
    ax = a3.Axes3D(pl.figure())
    ax.set_aspect('equal')
    
    face_count = 0
    line_count = 0
    point_count = 0

    d = t_scale
    for i in range(len(blocks)):        
        for fkey in blocks[i].faces():
            vkeys = blocks[i].face_vertices(fkey)
            vtx = []            
            for v in vkeys:
                vtx.append([blocks[i].vertex_coordinates(v)[0]*scale, blocks[i].vertex_coordinates(v)[1]*scale, blocks[i].vertex_coordinates(v)[2]*scale])
            poly = a3.art3d.Poly3DCollection([vtx])
            poly.set_facecolor(colors.rgb_to_hsv((1,.2,.1)))
            poly.set_alpha(0.2)
            poly.set_edgecolor('w')
            ax.add_collection3d(poly)

        centroid = blocks[i].center()
        
        # # draw mass vectors
        # if not block_model.vertex[i]['is_fixed']:            
        # number centroids
        ax.text(centroid[0]*scale+d, centroid[1]*scale+d, centroid[2]*scale+d, str(i), color='red')
        ax.scatter(centroid[0]*scale, centroid[1]*scale, centroid[2]*scale, c='b', marker='o', s=1)

        volume = blocks[i].volume()
        w = volume * v_scale
        a = Arrow3D([centroid[0]*scale,centroid[0]*scale],
                    [centroid[1]*scale,centroid[1]*scale],
                    [centroid[2]*scale,centroid[2]*scale-w],
                    mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
        ax.add_artist(a)
            
    for u, v in block_model.edges():
        # interfaces = block_model.edge[u][v]
        # for key in interfaces.keys():
        #     interface = interfaces[key]

        interface = block_model.edge[u][v]
            
        if interface['interface_type'] == 'face_face':
            # draw face -contacts
            face_count +=1
            coords = interface['interface_points']
            vtx = []
            for coord in coords:
                vtx.append([coord[0]*scale,coord[1]*scale, coord[2]*scale])
            poly = a3.art3d.Poly3DCollection([vtx])
            poly.set_facecolor(colors.rgb_to_hsv((.9,.9,.8)))
            poly.set_edgecolor('w')
            ax.add_collection3d(poly)


        # if interface['type']=='line':
        #     line_count +=1
        #     coords = interface['global_coords']
        #     x = []; y =[]; z=[]               
        #     for coord in coords:
        #         x.append(coord[0]*scale)
        #         y.append(coord[1]*scale)
        #         z.append(coord[2]*scale)
        #     x = np.array(x)
        #     y = np.array(y)
        #     z = np.array(z) 
        #     ax.plot(x, y, z) 
            
        # if interface['type']=='point':
        #     point_count +=1
        #     coord = interface['global_coords']                
        #     ax.scatter(coord[0][0]*scale, coord[0][1]*scale, coord[0][2]*scale, c='r', marker='o', s=20)
            
            
    print ' total count of interfaces'    
    print ' face_count  = ',   face_count                    
    print ' line_count  = ',   line_count                    
    print ' point_count = ',  point_count
        
    # plot range
    ax.set_xlim3d(xlim[0], xlim[1])
    ax.set_ylim3d(ylim[0], ylim[1])
    ax.set_zlim3d(zlim[0], zlim[1])

    #ax.set_aspect('equal')
    plt.show()