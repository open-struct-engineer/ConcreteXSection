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

# Bar Number, [Bar Dia (in), Bar Area (in2), Bar Weight (lb/ft), Metric Number]
ASTM_IMPERIAL_REBAR = {
                        3:[0.375,0.11,0.376,10],
                        4:[0.5,0.2,0.668,13],
                        5:[0.625,0.31,1.043,16],
                        6:[0.75,0.44,1.502,19],
                        7:[0.875,0.60,2.044,22],
                        8:[1,0.79,2.67,25],
                        9:[1.128,1,3.4,29],
                        10:[1.27,1.27,4.303,32],
                        11:[1.41,1.56,5.313,36],
                        14:[1.693,2.25,7.65,43],
                        18:[2.257,4.0,13.6,57]
                    }

# Bar Number, [Bar Dia (mm), Bar Area (mm2), Bar Weight (kg/m), Imperial Number]
ASTM_METRIC_REBAR = {
                        10:[9.5,71.0,0.56,3],
                        13:[12.7,129.0,0.994,4],
                        16:[15.9,199.0,1.552,5],
                        19:[19.1,284.0,2.235,6],
                        22:[22.2,387.0,3.042,7],
                        25:[25.4,510.0,3.973,8],
                        29:[28.7,645.0,5.06,9],
                        32:[32.3,819.0,6.404,10],
                        36:[35.8,1006.0,7.907,11],
                        43:[43.0,1452.0,11.38,14],
                        57:[57.3,2581.0,20.24,18]
                    }

class ASTM:

    def __init__(self, bar_number, material, units="Imperial/US"):

        self.material = material
        self.bar_number = bar_number
        self.units = units
        self.log = ""

        if self.units == "Imperial/US":
            self.As = ASTM_IMPERIAL_REBAR[self.bar_number][1]
            self.diameter = ASTM_IMPERIAL_REBAR[self.bar_number][0]
            self.weight_per_length = ASTM_IMPERIAL_REBAR[self.bar_number][2]
        elif self.units == "Metric":
            self.As = ASTM_METRIC_REBAR[self.bar_number][1]
            self.diameter = ASTM_METRIC_REBAR[self.bar_number][0]
            self.weight_per_length = ASTM_METRIC_REBAR[self.bar_number][2]
        else:
            self.As = 0
            self.diameter = 0
            self.weight_per_length = 0
            self.log = self.log + "No Unit System Defined -- all bar properties set to 0"      
    
    def convert_imperial(self):

        if self.units == "Imperial/US":
            pass
        else:
            self.bar_number = ASTM_METRIC_REBAR[self.bar_number][3]
            self.As = ASTM_IMPERIAL_REBAR[self.bar_number][1]
            self.diameter = ASTM_IMPERIAL_REBAR[self.bar_number][0]
            self.weight_per_length = ASTM_IMPERIAL_REBAR[self.bar_number][2]
    
    def convert_metric(self):
        if self.units == "Metric":
            pass
        else:
            self.bar_number = ASTM_IMPERIAL_REBAR[self.bar_number][3]
            self.As = ASTM_METRIC_REBAR[self.bar_number][1]
            self.diameter = ASTM_METRIC_REBAR[self.bar_number][0]
            self.weight_per_length = ASTM_METRIC_REBAR[self.bar_number][2]    