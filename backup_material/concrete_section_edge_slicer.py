# -*- coding: utf-8 -*-
"""
Created on Fri Feb 07 15:46:59 2020

@author: DonB
"""
from __future__ import division

import matplotlib.pyplot as plt

# Function to take x and y section coordinates and create lists of
# segment coordinates pairs that fit in the bounds of integration
# for the stress block

eu = 0.003 # ultimate strain
ec2 = 0.002 # parabolic strain upper bound

x = [3.698,17.840,-3.373,-17.515,3.698]
y = [-17.84,-3.698,17.515,3.373,-17.84]

strain_bounds = [ec2]

# Assumption 1: section rotated so strain only varies in y
# max y-coord is point of eu

na_depth = 7.5744 # depth of the neutral axis

y_na = max(y)-na_depth

y_bounds = [y_na]
y_bounds.extend([((i*na_depth)/eu)+y_na for i in strain_bounds])
y_bounds.append(max(y))

# work thru each section segment and pull out (x1,y1) (x2,y2) pairs
# for use in the stress block functions
stress_block_segments = []
for i in range(1,len(x)):
    
    x1 = x[i-1]
    y1 = y[i-1]
    x2 = x[i]
    y2 = y[i]
    
    if x1==x2:
        for j in enumerate(y_bounds):
            if j[0] == 0:
                pass
            else:
                if y2>=j[1]:
                    stress_block_segments.append([[x1,y_bounds[j[0]-1]],[x1,j[1]]])
                elif y1 >= j[1]:
                    stress_block_segments.append([[x1,j[1]],[x1,y_bounds[j[0]-1]]])
                
    elif y2==y1 and y2>y_na:
        
        if x2 > x1:
            stress_block_segments.append([[x2,y2],[x1,y1]])
        else:
            stress_block_segments.append([[x1,y1],[x2,y2]])
    elif y2>y_na or y1>y_na:
        
        m = (y2-y1)/(x2-x1)
        for j in enumerate(y_bounds):
            if j[0] == 0:
                pass
            else:
                x3 = ((y_bounds[j[0]-1]-y1)/m)+x1
                x4 = ((j[1]-y1)/m)+x1
                if y2>=j[1]:
                   stress_block_segments.append([[x3,y_bounds[j[0]-1]],[x4,j[1]]])
                elif y1>=j[1]:
                    stress_block_segments.append([[x4,j[1]],[x3,y_bounds[j[0]-1]]])
    
    else:
        pass
        
plt.close('all')

ax1 = plt.subplot2grid((2, 1), (0, 0))
ax2 = plt.subplot2grid((2, 1), (1, 0))
ax1.plot(x, y, 'c-')

colors = "bgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrkbgrk"

for k, segment in enumerate(stress_block_segments):
    xp = [i[0] for i in segment]
    yp = [j[1] for j in segment]
    
    ax2.plot(xp, yp, c=colors[k])
    
    label='s_'+str(k)
    
    ax2.text((xp[0]+xp[1])/2,(yp[0]+yp[1])/2,label)

plt.show()   
