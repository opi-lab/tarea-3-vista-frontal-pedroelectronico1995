from PIL import Image
import numpy
import sys

def normalize(points):
''' Normalize homogenous points'''
  for row in points:
    row /= points[-1]
  return points

def make_homog(points):
'''Make homogenous'''
  return numpy.vstack((points, numpy.ones((1, points.shape[1]))))

def Htransform(im, H, out_size):
  """Applies a homography transform to im"""
  pil_im = Image.fromarray(im)
  pil_size = out_size[1], out_size[0]
  return numpy.array(pil_im.transform(
    pil_size, Image.PERSPECTIVE, H.reshape(9)[0:8] / H[2,2], Image.LINEAR))

def H_from_points(fp, tp):
  '''Find H such that H * fp = tp.
  
  H has eight degrees of freedom, so this needs at least 4 points in fp and tp.
  '''
  if fp.shape != tp.shape:
    raise RuntimeError('number of points do not match')
    
    # COMPLETE THIS FUNCTION!!
    
    return H / H[2, 2]


if len(sys.argv) != 2:
  print 'usage: %prog image.jpeg'
  sys.exit(1)

imname = sys.argv[1]
im = array(Image.open(imname))
imshow(im)
gray()
corners = array(ginput(4))
# FIXME: sort corners, currently expects tl, bl, br, tr order.

# COMPLETE PROGRAM!!
