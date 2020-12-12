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

class VoidSectionPolygon:

    def __init__(self, x, y,  material, units="Imperial/US"):
        '''
        A section defined by (x,y) vertices

        the vertices should for a closed polygon.
        initialization will check is first and last coordinate are equal
        and if not will add an additional vertex equal to the first

        Inputs:

        x = a list of x coordinate values
        y = a list of y coordinate values

        Assumptions:

        x and y are of consistent units
        x and y form a closed polygon with no segment overlaps

        If solid = 1 then the coordinates will be ordered so the signed area
        is positive

        n = property multiplier
        '''

        self.material = material
        self.units = units
        self.shape='polygon'

        # check if a closed polygon is formed from the coordinates
        # if not add another x and y coordinate equal to the firts
        # coordinate x and y

        self.warnings = ''
        if x[0] == x[-1] and y[0] == y[-1]:
            pass
        else:
            x.append(x[0])
            y.append(y[0])

            self.warnings = self.warnings + '**User Verify** Shape was not closed, program attempted to close it.\n'

        # check the signed area of the coordinates, should be positive
        # for a solid shape. If not reverse the coordinate order

        self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
        self.area = self.area

        if self.area > 0:
            x.reverse()
            y.reverse()
            self.warnings = self.warnings + '**User Verify** Coordinate order reversed to make signed area negative for a void.\n'

            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
            self.area = self.area

        elif self.area == 0:
            self.warnings = self.warnings + '**User Verify** Area = 0 - verify defined shape has no overlapping segments.\n'

        else:
            pass

        self.x = [i for i in x]
        self.y = [j for j in y]

        if self.area == 0:
            pass
        else:
            self.calc_props()

    def calc_props(self):
            x = self.x
            y = self.y

            self.log = []
            self.log_strings = []

            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0

            self.log.append(self.area)
            self.log_strings.append('Area')

            # properties about the global x and y axis

            self.cx = sum([(x[i]+x[i+1])*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(6*self.area)
            self.cx = self.cx
            self.log.append(self.cx)
            self.log_strings.append('Cx')
            self.cy = sum([(y[i]+y[i+1])*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(6*self.area)
            self.cy = self.cy
            self.log.append(self.cy)
            self.log_strings.append('Cy')
            self.log.append('---')
            self.log_strings.append('Global Axis:')
            self.Ix = sum([((y[i]*y[i])+(y[i]*y[i+1])+(y[i+1]*y[i+1]))*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(12.0)
            self.Ix = self.Ix
            self.log.append(self.Ix)
            self.log_strings.append('Ix')
            self.Iy = sum([((x[i]*x[i])+(x[i]*x[i+1])+(x[i+1]*x[i+1]))*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(12.0)
            self.Iy = self.Iy
            self.log.append(self.Iy)
            self.log_strings.append('Iy')
            self.Ixy = sum([((x[i]*y[i+1])+(2*x[i]*y[i])+(2*x[i+1]*y[i+1])+(x[i+1]*y[i]))*(x[i]*y[i+1]-x[i+1]*y[i]) for i in range(len(x[:-1]))])/(24.0)
            self.Ixy = self.Ixy
            self.log.append(self.Ixy)
            self.log_strings.append('Ixy')
            self.Jz = self.Ix + self.Iy
            self.log.append(self.Jz)
            self.log_strings.append('Jz')
            self.sx_top = self.Ix / abs(max(y) - self.cy)
            self.log.append(self.sx_top)
            self.log_strings.append('Sx,top')
            self.sx_bottom = self.Ix / abs(min(y) - self.cy)
            self.log.append(self.sx_bottom)
            self.log_strings.append('Sx,botom')
            self.sy_right = self.Iy / abs(max(x) - self.cx)
            self.log.append(self.sy_right)
            self.log_strings.append('Sy,right')
            self.sy_left = self.Iy / abs(min(x) - self.cx)
            self.log.append(self.sy_left)
            self.log_strings.append('Sy,left')

            self.rx = math.sqrt(self.Ix/self.area)
            self.log.append(self.rx)
            self.log_strings.append('rx')
            self.ry = math.sqrt(self.Iy/self.area)
            self.log.append(self.ry)
            self.log_strings.append('ry')
            self.rz = math.sqrt(self.Jz/self.area)
            self.log.append(self.rz)
            self.log_strings.append('rz')

            # properties about the cross section centroidal x and y axis
            # parallel axis theorem Ix = Ixx + A*d^2
            # therefore to go from the global axis to the local
            # Ixx = Ix - A*d^2
            self.log.append('--')
            self.log_strings.append('Shape Centroidal Axis:')
            self.Ixx = self.Ix - (self.area*self.cy*self.cy)
            self.log.append(self.Ixx)
            self.log_strings.append('Ixx')
            self.Iyy = self.Iy - (self.area*self.cx*self.cx)
            self.log.append(self.Iyy)
            self.log_strings.append('Iyy')
            self.Ixxyy = self.Ixy - (self.area*self.cx*self.cy)
            self.log.append(self.Ixxyy)
            self.log_strings.append('Ixxyy')
            self.Jzz = self.Ixx + self.Iyy
            self.log.append(self.Jzz)
            self.log_strings.append('Jzz')
            self.sxx_top = self.Ixx / abs(max(y) - self.cy)
            self.log.append(self.sxx_top)
            self.log_strings.append('Sxx,top')
            self.sxx_bottom = self.Ixx / abs(min(y) - self.cy)
            self.log.append(self.sxx_bottom)
            self.log_strings.append('Sxx,bottom')
            self.syy_right = self.Iyy / abs(max(x) - self.cx)
            self.log.append(self.syy_right)
            self.log_strings.append('Syy,right')
            self.syy_left = self.Iyy / abs(min(x) - self.cx)
            self.log.append(self.syy_left)
            self.log_strings.append('Syy,left')

            self.rxx = math.sqrt(self.Ixx/self.area)
            self.log.append(self.rxx)
            self.log_strings.append('rxx')
            self.ryy = math.sqrt(self.Iyy/self.area)
            self.log.append(self.ryy)
            self.log_strings.append('ryy')
            self.rzz = math.sqrt(self.Jzz/self.area)
            self.log.append(self.rzz)
            self.log_strings.append('rzz')

            # Cross section principle Axis

            two_theta = math.atan((-1.0*2.0*self.Ixxyy)/(1E-16+(self.Ixx - self.Iyy)))
            temp = (self.Ixx+self.Iyy)/2.0
            temp2 = (self.Ixx-self.Iyy)/2.0
            I1 = temp + math.sqrt((temp2*temp2)+(self.Ixxyy*self.Ixxyy))
            I2 = temp - math.sqrt((temp2*temp2)+(self.Ixxyy*self.Ixxyy))

            self.log.append('--')
            self.log_strings.append('Shape Principal Axis:')
            self.Iuu = temp + temp2*math.cos(two_theta) - self.Ixxyy*math.sin(two_theta)
            self.log.append(self.Iuu)
            self.log_strings.append('Iuu')
            self.Ivv = temp - temp2*math.cos(two_theta) + self.Ixxyy*math.sin(two_theta)
            self.log.append(self.Ivv)
            self.log_strings.append('Ivv')
            self.Iuuvv = temp2*math.sin(two_theta) + self.Ixxyy*math.cos(two_theta)
            self.log.append(self.Iuuvv)
            self.log_strings.append('Iuuvv')

            if I1-0.000001 <= self.Iuu <= I1+0.000001:
                self.theta1 = math.degrees(two_theta/2.0)
                self.theta2 = self.theta1 + 90.0
            elif I2-0.000001 <= self.Iuu <= I2+0.000001:
                self.theta2 = math.degrees(two_theta/2.0)
                self.theta1 = self.theta2 - 90.0

            self.log.append(self.theta1)
            self.log_strings.append('Theta1,u')
            self.log.append(self.theta2)
            self.log_strings.append('Theta2,v')

    def calc_s_at_vertices(self):
        '''

        calculate the first moment of area at each vertex

        '''
        sx = []
        sy = []

        for y in self.y:
            if y == 0:
                y=0.00000000000001
            else:
                pass

            sx.append(self.Ixx / abs(y - self.cy))

        for x in self.x:
            if x == 0:
                x=0.00000000000001
            else:
                pass

            sy.append(self.Iyy / abs(x - self.cx))

        return sx,sy

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

    def transformed_vertices_degrees(self, xo, yo, angle, commit=0):
        '''
        given an angle in degrees
        and coordinate to translate about
        return the transformed values of the shape vertices
        '''
        theta = math.radians(angle)

        x_tr = [(x-xo)*math.cos(theta)+(y-yo)*math.sin(theta) for x,y in zip(self.x, self.y)]
        y_tr = [-1.0*(x-xo)*math.sin(theta)+(y-yo)*math.cos(theta) for x,y in zip(self.x, self.y)]

        # Commit transformation to Section
        if commit == 1:
            self.x = x_tr
            self.y = y_tr

            self.calc_props()
        else:
            pass

        return [x_tr, y_tr]

    def transformed_vertices_radians(self, xo, yo, angle, commit=0):
        '''
        given an angle in radians
        and coordinate to translate about
        return the transformed values of the shape vertices
        '''
        theta = angle

        x_tr = [(x-xo)*math.cos(theta)+(y-yo)*math.sin(theta) for x,y in zip(self.x, self.y)]
        y_tr = [-1.0*(x-xo)*math.sin(theta)+(y-yo)*math.cos(theta) for x,y in zip(self.x, self.y)]

        # Commit transformation to Section
        if commit == 1:
            self.x = x_tr
            self.y = y_tr

            self.calc_props()
        else:
            pass

        return [x_tr, y_tr]

    def translate_vertices(self, xo, yo, commit=0):
        '''
        give an x and y translation
        shift or return the shifted
        shape vertices by the x and y amount
        '''
        x_t = [x+xo for x in self.x]
        y_t = [y+yo for y in self.y]

        # Commit the translation to the shape
        if commit == 1:
            self.x = x_t
            self.y = y_t

            self.calc_props()
        else:
            pass

        return [x_t, y_t]

    def convert_metric(self):
        '''
        Assuming the original inputs were Imperial/US units
        convert the vertices to metric, mm and recompute
        the section properties

        '''

        'Check if already in metric'
        if self.units == "Metric":
            pass
        else:
            'Convert vertices from in to mm, 1:25.4'
            self.x = [i*25.4 for i in self.x]
            self.y = [j*25.4 for j in self.y]

            'recalc geometric properties'
            self.calc_props()

    def convert_imperial(self):
        '''
        Assuming the original inputs were Metric units
        convert the vertices to Imperial/US, inches and
        recompute the section properties.

        '''

        'Check if already in Imperial/US'
        if self.units == "Imperial/US":
            pass
        else:
            'Convert vertices from mm to in, 25.4:1'
            self.x = [i/25.4 for i in self.x]
            self.y = [j/25.4 for j in self.y]

            'recalc geometric properties'
            self.calc_props()

    def define_segments(self):
        '''
        return ordered coordinate pairs defining the line segments
        of each side of the section.
        '''
        self.segments = [[[self.x[i[0]],self.y[j[0]]],[self.x[i[0]+1],self.y[j[0]+1]]] for i,j in zip(enumerate(self.x[1:]),enumerate(self.y[1:]))]

        return self.segments
