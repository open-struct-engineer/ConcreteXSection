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