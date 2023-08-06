import numpy as np

def formu(x,y):
  """
  find the distance between two points
  Arguments:
      a: an integer
      b: an integer
  Returns:
      The distance between two points
  """
  forward = np.sqrt(np.square(y - x))
  backword = np.sqrt(np.square(((360 - (abs(max(x,y)))) + min(x,y))))
  lowest_distance=min(backword,forward)
  return lowest_distance


def HSV_distance(cc1,cc2):
  """
  calculate the distance between given HSV colour code
  Arguments:
      a: an list
      b: an list
  Returns:
      The distance between two HSV color code
  """
  if (cc1[0] < 361) and (cc2[0] < 361) and (cc1[1] < 101) and (cc2[1] < 101) and (cc1[2] < 101) and (cc2[2] < 101):
    forward = np.sqrt(np.square(cc2[0] - cc1[0]) + (np.square(cc2[1] - cc1[1])) + (np.square(cc2[2] - cc1[2])))
    maximun = max(cc1[0],cc2[0])
    minimun = min(cc1[0],cc2[0])
    backword = np.sqrt(np.square((((360 - (abs(maximun))) + minimun)) + (np.square(cc2[1] - cc1[1])) + (np.square(cc2[2] - cc1[2]))))
    lowest_distance=int(min(backword,forward))
  else:
    lowest_distance="entered colour code is not valid"
  return (lowest_distance)


def distance(ed1,ed2):
  """
  calculate the distance between given two integer or list
  Arguments:
      a: an integer or an list
      b: an integer or an list
  Returns:
      The distance between two points or list of points
  """
  if isinstance(ed1, list) and isinstance(ed2, list):
    if (max(ed1) < 361) and (max(ed2) < 361) and (len(ed1) == len(ed2)):
      result = sum([int(formu(ed1[i],ed2[i])) for i in range(len(ed1))])
    else:
      result="entered number exceed the limit 360 degree or given list is of different length"
  else:
    if (ed1 < 361) and (ed2 < 361):
      result = int(formu(ed1,ed2))
    else:
      result = "entered number exceed the limit 360 degree"
  return result

