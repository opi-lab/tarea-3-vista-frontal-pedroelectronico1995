# -*- coding: utf-8 -*-
"""
Created on Tue May 22 12:59:37 2018

@author: PEDRO NEL MENDOZA
"""

"""Create a function that takes the image coordinates of a square (or rectangular)
object (for example a book, a poster, or a 2D bar code) and estimates the transform
that takes the rectangle to a full on frontal view in a normalized coordinate system.
Use ginput() or the strongest Harris corners to find the points. 
 """

from matplotlib import pyplot as plt
from PIL import Image
import numpy  
import os

def normalize(points):
  # Normalize homogenous points
  for row in points:
    row /= points[-1]
  return points

def make_homog(points):
      """ Convert a set of points (dim*n array) to
      homogeneous coordinates. """
      
      return numpy.vstack((points, numpy.ones((1, points.shape[1]))))


def Htransform(im, H, out_size):
  # Applies a homography transform to im
  pil_im = Image.fromarray(im)
  pil_size = out_size[1], out_size[0]
  return numpy.array(pil_im.transform(
    pil_size, Image.PERSPECTIVE, H.reshape(9)[0:8] / H[2,2], Image.LINEAR))


def H_from_points(fp, tp):

  """ Find homography H, such that fp is mapped to tp 
    using the linear DLT method. Points are conditioned
    automatically. """

  num = len(fp.T)
      
  if fp.shape != tp.shape:
     raise RuntimeError('number of points do not match')

  # Condition points (important for numerical reasons)
  # --From points--
      
  average = numpy.mean(fp[:2], axis=1)
  maxstd = max(numpy.std(fp[:2], axis=1)) + 1e-9
  C1 = numpy.diag([1/maxstd, 1/maxstd, 1])
  C1[0][2] = -average[0]/maxstd
  C1[1][2] = -average[1]/maxstd
  fp = numpy.dot(C1,fp)

  # --to points--

  average = numpy.mean(tp[:2], axis=1)
  maxstd = max(numpy.std(tp[:2], axis=1)) + 1e-9
  C2 = numpy.diag([1/maxstd, 1/maxstd, 1])
  C2[0][2] = -average[0]/maxstd
  C2[1][2] = -average[1]/maxstd
  tp = numpy.dot(C2,tp)
      

  A = numpy.ones([3*num,9])
  array_zero = numpy.array([0,0,0])
  for i in range(num):            
      p = fp[:,i]
      A[3*i] = numpy.hstack([array_zero, -p, tp[1,i]*p])
      A[3*i+1] = numpy.hstack([p, array_zero, -tp[0,i]*p])
      A[3*i+2] = numpy.hstack([-tp[1,i]*p, tp[0,i]*p, array_zero])
            
  U,S,Vh = numpy.linalg.svd(A)
  p = Vh.T[:,-1]
  H = p.reshape(3,3)
      
  # decondition
  H = numpy.dot(numpy.linalg.inv(C2),numpy.dot(H,C1))
      
  # normalize and return
  return H / H[2,2]

im1 = numpy.array(Image.open(os.path.abspath('data/libro.jpg')).\
               convert('L'))

plt.figure('Imagen 1')
plt.axis('off'), plt.imshow(im1,cmap='gray')

# It uses the ginput function to acquire the 4 corners coordinates of book 
#x1 = np.array(plt.ginput(4,mouse_add=3,mouse_pop=1,mouse_stop=2)).T

fp = numpy.array([[ 465.34764815,  865.97495362,  163.78680563,  657.19453236],
               [82.81703591,  140.36892939,  453.74904507,  560.28151261]])

h, w = 400, 300
tp = numpy.array([[0,w,0,w],[0,0,h,h]])


xh1 = make_homog(fp)
xh2 = make_homog(tp)
H = H_from_points(xh2, xh1)
im_out = Htransform(im1, H, (h,w))

plt.figure()
plt.subplot(121), plt.imshow(im1,cmap='gray'), plt.axis('off')
plt.plot(fp[0],fp[1],'r.',markersize=6)
plt.subplot(122), plt.imshow(im_out,cmap='gray'), plt.axis('off')
plt.show()