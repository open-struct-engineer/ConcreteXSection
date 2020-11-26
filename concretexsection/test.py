# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 22:24:33 2020

@author: donni
"""

from geometry import ConcreteSection
 
x = [0,12,12,84,84,-16,-16,0,0]
y = [0,0,16,16,24,24,16,16,0]
 
material = 5000
Section = ConcreteSection.ConcreteSection(x, y, material)

print(Section.area)

segments = Section.define_segments()

alpha = 2.0737
x_t = 6
y_t = 12


Section.transformed_vertices_radians(x_t, y_t, alpha)

rotated_segment = Section.define_segments()

ASTM_IMPERIAL_REBAR = {
                        3:[0.375,0.11,0.376],
                        4:[0.5,0.2,0.668],
                        5:[0.625,0.31,1.043],
                        6:[0.75,0.44,1.502],
                        7:[0.875,0.60,2.044],
                        8:[1,0.79,2.67],
                        9:[1.128,1,3.4],
                        10:[1.27,1.27,4.303],
                        11:[1.41,1.56,5.313],
                        14:[1.693,2.25,7.65],
                        18:[2.257,4.0,13.6]
                    }

size = 4

print(ASTM_IMPERIAL_REBAR[size][1])