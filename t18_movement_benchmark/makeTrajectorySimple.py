import numpy as np
import matplotlib.pyplot as plt


step = 0.001
ts = np.arange(0, 0.1+step, step)

xs_source = np.zeros(len(ts))
ys_source = np.zeros(len(ts))
zs_source = -5 + 10*ts/0.1

xs_detector = -487 + 2000*ts
ys_detector = np.zeros(len(ts))
zs_detector = np.zeros(len(ts))



header = '''###### List of placement (translation and rotation) according to time
###### Column 1      is Time in s (second)
###### Column 2      is rotationAngle in degree
###### Columns 3,4,5 are rotation axis
###### Columns 6,7,8 are translation in mm
Time s
Rotation deg
Translation mm\n'''

rot = str(0)
axis1 = str(0)
axis2 = str(0)
axis3 = str(0)


f = open('data/moveSource.placements', 'w')
f.write(header)

for i in range(len(ts)):
    f.write(str(ts[i])+' '+rot+' '+axis1+' '+axis2+' '+axis3+' '+str(xs_source[i])+' '+str(ys_source[i])+' '+str(zs_source[i])+'\n')

f.close()



rot = str(90)
axis1 = str(0)
axis2 = str(1)
axis3 = str(0)


f = open('data/moveDetector.placements', 'w')
f.write(header)

for i in range(len(ts)):
    f.write(str(ts[i])+' '+rot+' '+axis1+' '+axis2+' '+axis3+' '+str(xs_detector[i])+' '+str(ys_detector[i])+' '+str(zs_detector[i])+'\n')

f.close()







