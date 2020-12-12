'''
BSD 3-Clause License
Copyright (c) 2020, open-struct-engineer developers
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from __future__ import division
import math

class ConcreteSectionCircle:

    def __init__(self, r, material, units="Imperial/US"):
        '''
        A circular section defined by a radius

        Inputs:

        r = radius

        Assumptions:

        (0,0) is the center of the circle

        Units Basis:
        Imperial/US: inches
        Metric: mm

        '''
        self.material = material
        self.units = units
        self.shape = 'circle'
        self.warnings=''
        self.r = r

    def calc_props(self):

        self.area = 2*math.pi*self.r*self.r

        self.cx = 0
        self.cy = 0
        self.Ix =(1/4.0)*math.pi*math.pow(self.r,4)
        self.Iy = self.Ix
        self.Ixy = 0
        self.Jz = self.Ix + self.Iy
        self.sx_top = self.Ix / (self.r - self.cy)
        self.sx_bottom = self.sx_top
        self.sy_right = self.Iy / (self.r - self.cx)
        self.sy_left = self.sy_right

        self.rx = math.sqrt(self.Ix/self.area)
        self.ry = math.sqrt(self.Iy/self.area)
        self.rz = math.sqrt(self.Jz/self.area)

        # properties about the cross section centroidal x and y axis
        # Circle is centered on (0,0), therefore
        # the properties above are the centroidal properties

        self.Ixx = self.Ix
        self.Iyy = self.Iy
        self.Ixxyy = self.Ixy
        self.Jzz = self.Ixx + self.Iyy
        self.sxx_top = self.sx_top
        self.sxx_bottom = self.sx_bottom
        self.syy_right = self.sy_right
        self.syy_left = self.sy_left

        self.rxx = self.rx
        self.ryy = self.ry
        self.rzz = self.rz

        # Cross section principle Axis

        two_theta = math.atan((-1.0*2.0*self.Ixxyy)/(1E-16+(self.Ixx - self.Iyy)))
        temp = (self.Ixx+self.Iyy)/2.0
        temp2 = (self.Ixx-self.Iyy)/2.0
        I1 = temp + math.sqrt((temp2*temp2)+(self.Ixxyy*self.Ixxyy))
        I2 = temp - math.sqrt((temp2*temp2)+(self.Ixxyy*self.Ixxyy))

        self.Iuu = temp + temp2*math.cos(two_theta) - self.Ixxyy*math.sin(two_theta)
        self.Ivv = temp - temp2*math.cos(two_theta) + self.Ixxyy*math.sin(two_theta)
        self.Iuuvv = temp2*math.sin(two_theta) + self.Ixxyy*math.cos(two_theta)

        if I1-0.000001 <= self.Iuu <= I1+0.000001:
            self.theta1 = math.degrees(two_theta/2.0)
            self.theta2 = self.theta1 + 90.0
        elif I2-0.000001 <= self.Iuu <= I2+0.000001:
            self.theta2 = math.degrees(two_theta/2.0)
            self.theta1 = self.theta2 - 90.0

    def parallel_axis_theorem(self, x, y):
        '''
        given a new global x,y coordinate for a new
        set of x, y axis return the associated Ix, Iy, and Ixy
        '''
        if self.area == 0:
            return [0,0,0]
        else:
            dx = self.cx - x
            dy = self.cy - y

            Ix = self.Ixx + (self.area*dy*dy)
            Iy = self.Iyy + (self.area*dx*dx)
            Ixy = self.Ixxyy + (self.area*dx*dy)

            return [Ix,Iy,Ixy]
